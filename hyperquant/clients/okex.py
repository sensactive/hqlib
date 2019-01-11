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
        ParamName.SYMBOLS: {
            "ltc_btc",
            "etc_btc",
        }

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
            ParamName.TIMESTAMP,
            ParamName.PRICE_OPEN,
            ParamName.PRICE_HIGH,
            ParamName.PRICE_LOW,
            ParamName.PRICE_CLOSE,
            ParamName.LEVEL,
        ],
    }

    def prepare_params(self, endpoint=None, params=None):

        resources, platform_params = super().prepare_params(endpoint, params)

        # (SYMBOL was used in URL path) (not necessary)
        if platform_params and ParamName.SYMBOL in platform_params:
            del platform_params[ParamName.SYMBOL]
        return resources, platform_params

    def _parse_item(self, endpoint, item_data):
        result = super()._parse_item(endpoint, item_data)

        if result and isinstance(result, Trade):
            # Determine direction
            result.direction = Direction.BUY if result.amount > 0 else Direction.SELL
            # Stringify and check sign
            result.price = str(result.price)
            result.amount = str(result.amount) if result.amount > 0 else str(-result.amount)
        return result



class OkexRESTClient(PrivatePlatformRESTClient):
    platform_id = Platform.OKEX
    version = "1"

    _converter_by_version = {
        "1": OkexRESTConverter
    }
    def get_symbols(self, version=None):
        return super().get_symbols(version="1")

    def fetch_trades(self, symbol, limit=None, from_item=None,
                           sorting=None, from_time=None, to_time=None, **kwargs):

        return super().fetch_trades_history(symbol, from_item, sorting=sorting,
                                          from_time=from_time, to_time=to_time, **kwargs)