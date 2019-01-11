from hyperquant.clients.bitfinex import BitfinexRESTClient
from hyperquant.clients.okex import OkexRESTClient
from hyperquant.clients.binance import BinanceRESTClient
# from hyperquant import *



res = BitfinexRESTClient()
res1 = OkexRESTClient()
res2 = BinanceRESTClient()

print(res1.fetch_candles(symbol="ltc_btc", interval="1min"))
# print(res.fetch_trades(symbol="ltcbtc"))
# print(res2.fetch_trades(symbol="LTCBTC"))