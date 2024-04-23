from datetime import datetime, timedelta, time
from volstreet.config import EXPIRY_FREQUENCIES
from volstreet import config
from volstreet.utils import current_time, parse_symbol
from volstreet.backtests.underlying_info import UnderlyingInfo, fetch_historical_expiry
from volstreet.backtests.framework import BackTester


class ProxyPriceFeed:
    data_bank = {}
    backtester = BackTester()
    _current_group = None

    @classmethod
    def request_grouped_prices_for_day(
        cls, underlying: UnderlyingInfo, day: datetime, **kwargs
    ):
        day_prices = cls.backtester.get_prices_for_day(underlying, day, **kwargs)
        day_prices_grouped = day_prices.groupby(day_prices.timestamp.dt.time)
        return day_prices_grouped

    @classmethod
    def update_prices(cls):
        prices_at_time = cls._current_group.get_group(config.backtest_state.time())
        price_dict = prices_at_time.to_dict(orient="records")
        cls.data_bank = {
            x["symboltoken"]: {
                "token": x["symboltoken"],
                "ltp": x["price"],
                "best_bid": x["price"],
                "best_ask": x["price"],
                "best_bid_qty": 0,
                "best_ask_qty": 0,
                "last_traded_datetime": x["timestamp"],
            }
            for x in price_dict
        }


class ProxyFeeds:
    price_feed = ProxyPriceFeed
    order_feed = []

    @classmethod
    def price_feed_connected(cls):
        return bool(cls.price_feed.data_bank)


def get_symbol_token(name=None, expiry=None, strike=None, option_type=None):
    if expiry is None and strike is None and option_type is None:
        return name.upper(), name.upper()
    else:
        symbol = f"{name.upper()}{expiry.upper()}{int(strike)}{option_type.upper()}"
        return symbol, symbol


def get_expiry_dates(expiry_frequency: int):
    expiry_frequencies = {v: k for k, v in EXPIRY_FREQUENCIES.items()}
    underlying = expiry_frequencies[expiry_frequency]
    expiries = fetch_historical_expiry(
        underlying, current_time(), threshold_days=0, n_exp=4
    )
    return expiries


def get_base(name, expiry):
    return UnderlyingInfo(name).base


def get_lot_size(*args, **kwargs):
    return 1


def identify_average_prices(instruments, avg_prices: dict[str, float]) -> dict:

    average_price_dict = {}  # The new dict to be returned
    for instr in instruments:
        if hasattr(instr, "call_option") and hasattr(instr, "put_option"):
            call_instr, put_instr = instr.call_option, instr.put_option
            average_price_dict[instr] = (
                avg_prices[call_instr.symbol],
                avg_prices[put_instr.symbol],
            )
        else:
            average_price_dict[instr] = avg_prices[instr.symbol]

    return average_price_dict


def simulate_execution(order: dict):

    price = order["price"]
    index, expiry, strike, option_type = parse_symbol(order["symboltoken"])
    value = order["quantity"] * price * (1 if order["transactiontype"] == "BUY" else -1)
    order_details = {
        "timestamp": current_time(),
        "index": index,
        "expiry": expiry,
        "strike": strike,
        "option_type": option_type,
        "action": order["transactiontype"],
        "price": price,
        "quantity": order["quantity"],
        "value": value,
        "token": order["symboltoken"],
    }
    return order_details


def execute_instructions(instructions: dict, *args, **kwargs):
    orders = []
    for instrument, params in instructions.items():
        if hasattr(instrument, "call_token") and hasattr(instrument, "put_token"):
            call_price = ProxyFeeds.price_feed.data_bank[instrument.call_token]["ltp"]
            put_price = ProxyFeeds.price_feed.data_bank[instrument.put_token]["ltp"]
            orders.extend(
                instrument.generate_order_params(
                    **params, price=(call_price, put_price)
                )
            )
        else:
            price = ProxyFeeds.price_feed.data_bank[instrument.token]["ltp"]
            orders.extend(instrument.generate_order_params(**params, price=price))
    orders = [simulate_execution(order) for order in orders]
    ProxyFeeds.order_feed.extend(orders)
    average_prices = {order["token"]: order["price"] for order in orders}
    return identify_average_prices(instructions, average_prices)


def sleep_until_next_action(
    interval_minutes: int, exit_time: tuple[int, int], *args, **kwargs
):
    interval_minutes = max(1, interval_minutes)
    config.backtest_state += timedelta(minutes=interval_minutes)
    config.backtest_state = min(
        config.backtest_state,
        datetime.combine(config.backtest_state.date(), time(*exit_time)),
    )
    ProxyPriceFeed.update_prices()


def exit_on_error(func):
    return func


def increase_robustness(func):
    return func


def notify_pnl(*args, **kwargs):
    pass
