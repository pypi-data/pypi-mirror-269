import json
from json import JSONDecodeError
from binance.api import API
import logging
import requests
import multitasking
from time import sleep

from binance.error import ClientError, ServerError

from .constant import GrantType, RetCode

class DeribitAPI(API):
    """API base class

    Keyword Args:
        base_url (str, optional): the API base url, useful to switch to testnet, etc. By default it's https://api.binance.com
        timeout (int, optional): the time waiting for server response, number of seconds. https://docs.python-requests.org/en/master/user/advanced/#timeouts
        proxies (obj, optional): Dictionary mapping protocol to the URL of the proxy. e.g. {'https': 'http://1.2.3.4:8080'}
        show_limit_usage (bool, optional): whether return limit usage(requests and/or orders). By default, it's False
        show_header (bool, optional): whether return the whole response header. By default, it's False
        private_key (str, optional): RSA private key for RSA authentication
        private_key_pass(str, optional): Password for PSA private key
    """
    
    running: bool = True
    refresh_token: str = ''
    expires_in: int = 0

    def __init__(
        self,
        api_key=None,
        api_secret=None,
        base_url='https://test.deribit.com/api/v2',
        timeout=None,
        proxies=None,
        show_limit_usage=False,
        show_header=False,
        private_key=None,
        private_key_pass=None,
        client_id=None,
        client_secret=None
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.timeout = timeout
        self.proxies = None
        self.show_limit_usage = False
        self.show_header = False
        self.private_key = private_key
        self.private_key_pass = private_key_pass
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json;charset=utf-8"
            }
        )

        if show_limit_usage is True:
            self.show_limit_usage = True

        if show_header is True:
            self.show_header = True

        if type(proxies) is dict:
            self.proxies = proxies

        self._logger = logging.getLogger(__name__)
        self.auth()
    
    def _handle_exception(self, response):
        status_code = response.status_code
        if status_code < 400:
            return
        if 400 <= status_code < 500:
            try:
                err = json.loads(response.text)['error']
            except JSONDecodeError:
                raise ClientError(
                    status_code, None, response.text, None, response.headers
                )
            error_data = err
            if "data" in err:
                error_data = err["data"]
            raise ClientError(
                status_code, err["code"], error_data, response.headers, error_data
            )
        raise ServerError(status_code, response.text)
    
    def stop(self):
        self.running = False
    
    def auth(self, grant_type=GrantType.CLIENT_CREDENTIALS, auto_refresh=True):
        params = {'grant_type': grant_type.value}
        if grant_type == GrantType.CLIENT_CREDENTIALS:
            params.update({'client_id': self.client_id, 'client_secret': self.client_secret})
        elif grant_type == GrantType.REFRESH_TOKEN:
            params.update({'refresh_token': self.refresh_token})

        data = self.send_request('GET', '/public/auth', params)
        if data.get('result'):
            self.session.headers.update({
                "Authorization": f"{data['result']['token_type']} {data['result']['access_token']}"
            })
            self.refresh_token = data['result']['refresh_token']
            self.expires_in = data['result']['expires_in']
        self._logger.info(f'auth:{data}')
        # print(data)
        
        if auto_refresh:
            self.auth_interval()

    @multitasking.task
    def auth_interval(self):
        while self.running:
            sleep(self.expires_in - 60)
            self.auth(grant_type=GrantType.REFRESH_TOKEN, auto_refresh=False)
            

    def request_path(self, method, url_path, params):
        try:
            data = self.send_request(method, url_path, params)
        except Exception as e:
            return RetCode.ERROR, e.error_data
        
        reuslt = data and data.get('result') or None
        
        return RetCode.OK, reuslt 
    
    def get_instrument(self, instrument_name):
        url_path = '/public/get_instrument'
        return self.request_path('GET', url_path, {'instrument_name': instrument_name})

    def get_open_orders(self, instrument_name):
        url_path = '/private/get_open_orders_by_instrument'
        return self.request_path('GET', url_path, {'instrument_name': instrument_name})
    
    def get_position(self, instrument_name):
        url_path = '/private/get_position'
        return self.request_path('GET', url_path, {'instrument_name': instrument_name})
    
    

if __name__ == '__main__':
    import json
    with open('config.json') as fs:
        config = json.load(fs)
    api = DeribitAPI(base_url='https://test.deribit.com/api/v2', client_id=config['client_id'], client_secret=config['client_secret'])
    instrument_name = "BTC-26APR24-66000-C"
    # ret_code, data = api.get_open_orders(instrument_name)
    # print(ret_code, data)
    ret_code, data = api.get_instrument(instrument_name)
    print(ret_code, data)
    # ret_code, data = api.get_position(instrument_name)
    # print(ret_code, data)

 
