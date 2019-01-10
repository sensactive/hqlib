import hashlib
import hmac

from hyperquant.api import Platform, Sorting, Interval, Direction, OrderType
from hyperquant.clients import WSClient, Endpoint, Trade, Error, ErrorCode, \
    ParamName, WSConverter, RESTConverter, PrivatePlatformRESTClient, MyTrade, Candle, Ticker, OrderBookItem, Order, \
    OrderBook, Account, Balance



class OkexRESTConverter(RESTConverter):

    # Main params:
    base_url = "https://www.okex.com/api/v{version}/"

    # Settings:

    # Converting info:
    # For converting to platform
    endpoint_lookup = {
        Endpoint.TRADE: "trades.do",
        Endpoint.TRADE_HISTORY: "trades.do",  #???

        Endpoint.CANDLE: "kline.do"
    }

    param_name_lookup = {
        ParamName.SYMBOL: "symbol",

        ParamName.INTERVAL: "type",
        ParamName.TIMESTAMP: "since",
    }
    param_value_lookup = {
        Interval.MIN_1: "1min",
        Interval.MIN_3: "3min",
        Interval.MIN_5: "5min",
        Interval.MIN_15: "15min",
        Interval.MIN_30: "30min",
        Interval.HRS_1: "1hour",
        Interval.HRS_2: "2hour",
        Interval.HRS_4: "4hour",
        Interval.HRS_6: "6hour",
        Interval.HRS_12: "12hour",
        Interval.DAY_1: "1day",
        Interval.WEEK_1: "1week",
    }
    max_limit_by_endpoint = {
        Endpoint.TRADE: 1000,
        Endpoint.TRADE_HISTORY: 1000,

        Endpoint.CANDLE: 1000,
    }
    param_lookup_by_class = {
        # Error
        Error: {
            "code": "code",
            "msg": "message",
        },
        # Data
        Trade: {
            "time": ParamName.TIMESTAMP,
            "id": ParamName.ITEM_ID,
            "price": ParamName.PRICE,
            "qty": ParamName.AMOUNT,
            # "isBuyerMaker": "",
            # "isBestMatch": "",
        },
        Candle: [
            ParamName.TIMESTAMP,
            None,
            None,
            None,
            None,
            None,  # ParamName.AMOUNT,  # only volume present
            None,
            None,
            None,
            # ParamName.INTERVAL,
        ],
    }