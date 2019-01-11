from hyperquant.clients.bitfinex import BitfinexRESTClient
from hyperquant.clients.okex import OkexRESTClient
from hyperquant import *



res = BitfinexRESTClient()
res1 = OkexRESTClient()

print(res.fetch_trades(symbol="ltcbtc"))