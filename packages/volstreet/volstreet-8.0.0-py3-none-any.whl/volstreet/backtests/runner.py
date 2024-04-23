from datetime import datetime, time
from typing import Callable
import pandas as pd
import os
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
from volstreet import config
from volstreet.utils import make_directory_if_needed, current_time
from volstreet.historical_info import market_days
from volstreet.backtests.framework import nav_drawdown_analyser
from volstreet.backtests.underlying_info import UnderlyingInfo
from volstreet.backtests.proxy_functions import ProxyPriceFeed, ProxyFeeds


class Runner:
    def __init__(
        self,
        underlying: UnderlyingInfo,
        start_date: "datetime.date",
        end_date: "datetime.date",
        strategy: Callable,
        parameters: dict,
        start_time: "datetime.time" = time(9, 16),
        end_directory: str = None,
    ):
        self.underlying = underlying
        self.start_date = start_date
        self.end_date = end_date
        self.strategy = strategy
        self.parameters = parameters
        self.start_time = start_time
        self.end_directory = end_directory

        # Post initialization
        self.price_feed = ProxyPriceFeed
        self.Index = __import__("volstreet.trade_interface").Index
        self.end_directory = self.make_result_directory(end_directory)

    def make_result_directory(self, end_directory):
        # Making a directory to store the results
        strategy = self.strategy.__name__
        index_strategy_directory = f"backtester\\{self.underlying.name}_{strategy}\\"
        if end_directory is None:
            folder_number = len(os.listdir(index_strategy_directory)) + 1
            end_directory = f"test_{folder_number}\\"

        end_directory = os.path.join(index_strategy_directory, f"{end_directory}\\")
        make_directory_if_needed(end_directory)
        return end_directory

    def run(
        self,
        only_expiry: bool = False,
        num_strikes: int = 30,
        num_exp: int = 2,
        start_time: tuple[int, int] = (9, 16),
        end_time: tuple[int, int] = (15, 30),
    ) -> None:
        valid_range = pd.date_range(self.start_date, self.end_date)
        valid_range = [day.date() for day in valid_range if day.date() in market_days]

        if only_expiry:
            target_days = map(lambda x: x.date(), self.underlying.expiry_dates)
            target_days = [day for day in target_days if day in valid_range]
        else:
            target_days = valid_range

        # Dumping the parameters in the directory
        with open(os.path.join(self.end_directory, "parameters.json"), "w") as f:
            json.dump(self.parameters, f)

        with ProcessPoolExecutor(max_workers=4) as executor:
            daily_prices = [
                executor.submit(
                    self.price_feed.request_grouped_prices_for_day,
                    self.underlying,
                    day,
                    num_strikes=num_strikes,
                    num_exp=num_exp,
                    start_time=start_time,
                    end_time=end_time,
                )
                for day in target_days
            ]

            error_list = []
            for daily_prices in as_completed(daily_prices):
                try:
                    date = daily_prices.result().timestamp.first().iloc[0].date()
                    self.price_feed._current_group = (
                        daily_prices.result()
                    )  # Updating prices
                    config.backtest_state = datetime.combine(
                        date, self.start_time
                    )  # State changes to the next day
                    self.price_feed.update_prices()  # data_bank gets updated
                    updated_index_instance = self.Index(
                        self.underlying.name
                    )  # Index instance gets updated
                    ProxyFeeds.order_feed = []  # Order feed gets reset
                    self.strategy(
                        underlying=updated_index_instance,
                        data_directory=self.end_directory,
                        **self.parameters,
                    )
                    day_result = ProxyFeeds.order_feed
                    result = pd.DataFrame(day_result)
                    filename = os.path.join(
                        self.end_directory, f"{current_time().strftime('%d-%m-%Y')}.csv"
                    )
                    result.to_csv(filename)
                except Exception as e:
                    config.logger.error(
                        f"Error in running the strategy {self.strategy.__name__} for {date}: {e}",
                        traceback=True,
                    )
                    error_list.append(date)

            config.logger.info(
                f"Finished running the strategy {self.strategy.__name__} from {self.start_date} to {self.end_date}. "
                f"Total errors: {len(error_list)}. Error days: {error_list}"
            )


def get_parallel_runners(
    underlying: UnderlyingInfo,
    start_date: datetime,
    end_date: datetime,
    strategy,
    parameters,
    end_directory,
):
    entire_date_range = pd.date_range(start_date, end_date, freq="B")
    if len(entire_date_range) < 6:
        return [
            Runner(
                underlying=underlying,
                start_date=start_date,
                end_date=end_date,
                strategy=strategy,
                parameters=parameters,
                end_directory=end_directory,
            )
        ]
    date_ranges = np.array_split(entire_date_range, 6)  # 6 processes
    runners = []
    for date_range in date_ranges:
        runner = Runner(
            underlying=underlying,
            start_date=date_range[0],
            end_date=date_range[-1],
            strategy=strategy,
            parameters=parameters,
            end_directory=end_directory,
        )
        runners.append(runner)
    return runners


def consolidate_backtest(path: str) -> pd.DataFrame:
    df = pd.DataFrame()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            day_df = pd.read_csv(
                f"backtester\\NIFTY_delta_hedged_strangle\\test_1\\{file}"
            )
            df = pd.concat([df, day_df])
    df["quantity"] = np.where(
        df["action"] == "BUY", 1 * df["quantity"], -1 * df["quantity"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    df = df.iloc[:, 1:]
    return df


def describe_backtest(dataframe: pd.DataFrame) -> pd.DataFrame:
    # -1 because we are selling the strangle
    all_days = dataframe.groupby(dataframe.index.date).agg(
        {"quantity": "sum", "value": ["sum", lambda x: x.abs().sum()]}
    )
    config.logger.info(f"Total number of days: {len(all_days)}")
    all_days.columns = ["quantity", "profit", "turnover"]
    all_days["exposure"] = 10000000
    all_days["profit"] *= -1
    all_days["profit_percentage"] = (all_days["profit"] / all_days["exposure"]) * 100
    invalid_days = all_days.query("quantity != 0").index
    all_days = all_days[all_days["quantity"] == 0].drop(columns="quantity")
    config.logger.info(
        f"Number of valid days: {len(all_days)}. Invalid days: {invalid_days}"
    )
    config.logger.info(
        f"Profit Margin: {(all_days.profit.sum() / all_days.turnover.sum()) * 100: 0.2f}%"
    )
    all_days = nav_drawdown_analyser(
        all_days, column_to_convert="profit_percentage", profit_in_pct=True
    )
    return all_days
