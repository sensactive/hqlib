import hashlib
import hmac

from hyperquant.api import Platform, Sorting, Interval, Direction
from hyperquant.clients import WSClient, Endpoint, Trade, ParamName, \
                    WSConverter, RESTConverter, PrivatePlatformRESTClient, Candle



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
        ParamName.FROM_ITEM: "since",


        ParamName.INTERVAL: "type",
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
        ParamName.SYMBOLS: [
            "ltc_btc",
            "etc_btc",
        ]

    }
    max_limit_by_endpoint = {
        Endpoint.TRADE: 1000,
        Endpoint.TRADE_HISTORY: 1000,

        Endpoint.CANDLE: 1000,
    }
    param_lookup_by_class = {
        # Data
        Trade: {
            "tid": ParamName.ITEM_ID,
            "price": ParamName.PRICE,
            "amount": ParamName.AMOUNT,
            "date": ParamName.TIMESTAMP,
            "type": ParamName.DIRECTION,
        },
        Candle: [
            ParamName.FROM_TIME,
            ParamName.PRICE_OPEN,
            ParamName.PRICE_HIGH,
            ParamName.PRICE_LOW,
            ParamName.PRICE_CLOSE,
            ParamName.LEVEL,
        ],
    }




class OkexRESTClient(PrivatePlatformRESTClient):
    platform_id = Platform.OKEX
    version = "1"

    _converter_class_by_version = {
        "1": OkexRESTConverter,
    }




