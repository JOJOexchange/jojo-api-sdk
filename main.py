import os
import datetime
import json
import requests
import urllib
from web3.auto import w3
from dotenv import load_dotenv
load_dotenv()

class JojoAPI:
    def __init__(self, base_url: str, private_key: str):
        self.base_url = base_url
        self.private_key = private_key
        self.public_key = self.get_public_key_from_private()
        self.headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0'
        }

    def get_public_key_from_private(self) -> str:
        return w3.eth.account.from_key(self.private_key).address

    def sign_message(self, message: str) -> bytes:
        message_hash = w3.keccak(text=message)
        signed_message = w3.eth.account._sign_hash(message_hash, private_key=self.private_key)
        return signed_message.signature

    def _prepare_request(self, payload: dict = None) -> tuple:
        if payload is None:
            payload = {}
        timestamp = int(datetime.datetime.now().timestamp() * 1000)
        payload['timestamp'] = timestamp
        
        sorted_params = json.loads(json.dumps(payload, sort_keys=True))
        url_params = urllib.parse.urlencode(sorted_params)
        
        message = '\x19Ethereum Signed Message:\n{}{}'.format(len(url_params), url_params)
        signature = self.sign_message(message)
        
        return url_params, signature

    def authenticate(self, method: str, endpoint: str, payload: dict = None):
        url_params, signature = self._prepare_request(payload)
        url = self.base_url + endpoint
        post_data = url_params + '&signature={}'.format(signature.hex())

        if method.lower() == 'get':
            return requests.get(url, post_data, headers=self.headers)
        elif method.lower() == 'post':
            return requests.post(url, post_data, headers=self.headers)
        elif method.lower() == 'delete':
            return requests.delete(url + '?' + post_data, headers=self.headers)

    def _handle_request(self, method: str, endpoint: str, payload: dict = None):
        if payload is None:
            payload = {}
        if payload.get('account') is None:
            payload['account'] = self.public_key
        
        response = self.authenticate(method, endpoint, payload)
        return response.json() if method != 'delete' else response

    def get_time(self) -> dict:
        return requests.get(f"{self.base_url}/v1/time").json()

    def get_exchange_info(self) -> dict:
        return requests.get(f"{self.base_url}/v1/exchangeInfo").json()

    def get_orderbook(self, **kwargs) -> dict:
        return requests.get(
            f"{self.base_url}/v1/orderbook",
            urllib.parse.urlencode(kwargs)
        ).json()

    def post_account(self, **kwargs) -> dict:
        return self._handle_request('post', '/v1/account', kwargs)

    def get_account(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/account', kwargs)
    
    def post_order_build(self, **kwargs) -> dict:
        return self._handle_request('post', '/v1/order/build', kwargs)

    def post_order(self, **kwargs) -> dict:
        order_build = self._handle_request('post', '/v1/order/build', kwargs)
        if order_build.get('orderHash') is None:
            return order_build
            
        order_hash = order_build['orderHash']
        kwargs.update({
            'info': order_build['order']['info'],
            'gasFeeQuotation': order_build['gasFeeQuotation'],
            'orderSignature': w3.eth.account._sign_hash(
                order_hash, 
                private_key=self.private_key
            ).signature.hex()
        })
        
        return self._handle_request('post', '/v1/order', kwargs)
    
    def delete_order(self, **kwargs) -> dict:
        return self._handle_request('delete', '/v1/order', kwargs)
    
    def get_order(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/order', kwargs)
    
    def get_open_order(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/openOrder', kwargs)
    
    def get_open_orders(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/openOrders', kwargs)
    
    def get_user_trades(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/userTrades', kwargs)
    
    def delete_all_open_orders(self, **kwargs) -> dict:
        return self._handle_request('delete', '/v1/allOpenOrders', kwargs)

    def get_positions(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/positions', kwargs)
    
    def get_trades(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/trades', kwargs)
    
    def get_history_orders(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/historyOrders', kwargs)

    def get_klines(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/klines', kwargs)
    
    def get_mark_price_klines(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/offchainMarkPriceWithVolKlines', kwargs)

    def get_funding_rate(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/fundingRate', kwargs)
    
    def get_risky_accounts(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/riskyAccounts', kwargs)
    
    def get_risky_accounts_history(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/riskyAccounts', kwargs)
    
    def get_historical_trades(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/historicalTrades', kwargs)
    
    def get_incomes(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/incomes', kwargs)
    
    def get_balances(self, **kwargs) -> dict:
        return self._handle_request('get', '/v1/balances', kwargs)
    
if __name__ == '__main__':
    api_client = JojoAPI(
        os.environ.get('JOJO_API_BASE_URL'),
        os.environ.get('ACCOUNT_PRIVATE_KEY')
    )

    # account api
    # print("register account: ", api_client.post_account())
    print("get account:", api_client.get_account())

    # system api
    # print("time: ", api_client.get_time())
    # print("exchange info: ", api_client.get_exchange_info())

    # public api
    # print("orderbook: ", api_client.get_orderbook(marketId='btcusdc'))
    # print("trades: ", api_client.get_trades(marketId='ethusdc'))
    # print("klines: ", api_client.get_klines(marketId='ethusdc', interval='1D'))
    # print("mark price klines: ", api_client.get_mark_price_klines(marketId='btcusdc', interval='1D'))
    # print("funding rate: ", api_client.get_funding_rate(marketId='btcusdc', limit=500))
    # print("risky accounts: ", api_client.get_risky_accounts())

    # order api
    # print("post order build: ", api_client.post_order_build(marketId='ethusdc', side='BUY', orderType='LIMIT', amount=0.5, price=1800, timeInForce='GTC'))
    # print("post order: ", api_client.post_order(marketId='ethusdc', side='BUY', orderType='LIMIT', amount=0.5, price=1800, timeInForce='GTC'))
    # print("delete order: ", api_client.delete_order(marketId='ethusdc', orderId='275287091667264'))
    # print("delete all open orders: ", api_client.delete_all_open_orders(marketId='ethusdc'))
    # print("history orders: ", api_client.get_history_orders(marketId='ethusdc'))
    # print("historical trades: ", api_client.get_historical_trades(marketId='btcusdc'))
    # print("order: ", api_client.get_order(marketId='ethusdc', orderId='274991744483648'))
    # print("open order: ", api_client.get_open_order(marketId='ethusdc', orderId='274991744483648'))
    # print("open orders: ", api_client.get_open_orders(marketId='ethusdc'))
    # print("user trades: ", api_client.get_user_trades(marketId='ethusdc'))
    # print("incomes: ", api_client.get_incomes(marketId='ethusdc'))
    # print("balances: ", api_client.get_balances())
    # print("positions: ", api_client.get_positions())

    # # authorized from other subaccount e.g. 0x73B14CD04Ef491407C9667D1e02d985cCeAB8270
    #print("build order: ", api_client.post_order_build(marketId='ethusdc', side='BUY', orderType='LIMIT', amount=0.5, price=1800, timeInForce='GTC', account='0x73B14CD04Ef491407C9667D1e02d985cCeAB8270'))
    # print("post order: ", api_client.post_order(marketId='ethusdc', side='BUY', orderType='LIMIT', amount=0.5, price=1800, timeInForce='GTC', account='0x73B14CD04Ef491407C9667D1e02d985cCeAB8270'))
    # print("delete order: ", api_client.delete_order(marketId='ethusdc', orderId='51597754450176', account='0x73B14CD04Ef491407C9667D1e02d985cCeAB8270'))
    # print("delete all open orders: ", api_client.delete_all_open_orders(marketId='ethusdc', account='0x73B14CD04Ef491407C9667D1e02d985cCeAB8270'))
    # print("history orders: ", api_client.get_history_orders(marketId='ethusdc', account='0x73B14CD04Ef491407C9667D1e02d985cCeAB8270'))
    # print("get order: ", api_client.get_order(marketId='ethusdc', orderId='51597754450176', account='0x73B14CD04Ef491407C9667D1e02d985cCeAB8270'))
    # print("get open order: ", api_client.get_open_order(marketId='ethusdc', orderId='51597754450176', account='0x73B14CD04Ef491407C9667D1e02d985cCeAB8270'))
    # print("open orders: ", api_client.get_open_orders(marketId='ethusdc', account='0x73B14CD04Ef491407C9667D1e02d985cCeAB8270'))
    # print("user trades: ", api_client.get_user_trades(marketId='ethusdc', account='0x73B14CD04Ef491407C9667D1e02d985cCeAB8270'))
    # print("incomes: ", api_client.get_incomes(marketId='ethusdc', account='0x73B14CD04Ef491407C9667D1e02d985cCeAB8270'))
    # print("balances: ", api_client.get_balances(account='0x73B14CD04Ef491407C9667D1e02d985cCeAB8270'))
    # print("positions: ", api_client.get_positions(account='0x73B14CD04Ef491407C9667D1e02d985cCeAB8270'))
