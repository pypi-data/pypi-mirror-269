import json
import os.path
import time

import requests
from requests import Response
from urllib3.exceptions import NewConnectionError

TESTS = ['http://localhost:9090', 'http://127.0.0.1:9090', 'http://0.0.0.0:9090', 'http://proxy_service:9090',
         'http://xclash:9090', 'http://proxy_service_provider:9090']


class ClashAPIErr(Exception):
    ...


class ProxyNotFound(ClashAPIErr):
    ...


class TimeoutProxy(ClashAPIErr):
    ...


class ProxyDelay(ClashAPIErr):
    ...


class APIBase:
    bind_log_fn = None

    def __init__(self):
        self.error_count = 0
        self.bind_log_fn = None

    def bind_log(self, dn):
        self.bind_log_fn = dn

    def switch_failure(self):
        self.error_count += 1
        if self.error_count > 10:
            self.error_count = 0
            self.errlog(
                "[CLASHX] Tried 10 vpn access point and it keeps fails. Please double check the vpn health from the provider")

    def errlog(self, msg: str):
        if self.bind_log_fn is not None:
            self.bind_log_fn(msg)
        else:
            print(msg)


class ClashAPI:
    _ps: list
    url: str
    secret_bearer: str
    conf: dict
    available: list
    sock: str
    httpproxy: str
    work: bool
    loaded: bool
    health: int
    _status: int
    # 0: off, 1: rotating, 2: rotate done
    error_count: int
    vpn_iter_n: int
    store_vpn_delays: str

    def __init__(self):
        self.url = ""
        self.secret_bearer = ""
        self.conf = {}

    def read_connection_file(self, file_path: str):
        self.store_vpn_delays = file_path
        self._read_connections()

    def _read_connections(self):
        if os.path.isfile(self.store_vpn_delays) is False:
            print("[CLASHX] connection file is not found")
            return
        io = open(self.store_vpn_delays, 'r')
        try:
            self.available = json.loads(io.read())
            io.close()
        except json.JSONDecodeError:
            print("[CLASHX] decode json file error")

    def test_protocol(self):
        n = 0
        err = 0

        while True:
            try:
                print("[CLASHX] looking up clash X environment port.")
                b = n % len(TESTS)
                self.url = TESTS[b]
                self.conf = self.get_conf()
                print(f"[CLASHX] successfully using {self.url}")
                break

            except requests.exceptions.ConnectionError:
                n += 1
                err += 1
                print(f"[CLASHX][ERROR] {self.url} is not open. Keep scan for the next port.")
                if err > 5:
                    break
                time.sleep(1)
                continue

            except Exception:
                n += 1
                err += 1
                print(f"[CLASHX][ERROR] {self.url} is not open. Keep scan for the next port.")
                if err > 5:
                    break
                time.sleep(1)
                continue

    def _get_base(self, endpoint, method='GET', data=None):
        response = self._wrap_base(endpoint, method, data)
        if response.status_code > 300:
            raise Exception(f'[CLASHX][ERROR] Request failed with status code {response.status_code}')
        else:
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 204:
                return {}
            else:
                return {}

    def _wrap_base(self, endpoint: str, method: str, data=None) -> Response:
        _url = f'{self.url}/{endpoint}'
        __header = {
            'Content-type': 'application/json'
        }
        if self.secret_bearer != '':
            __header.update({
                'Authorization': f'Bearer {self.secret_bearer}'
            })
        if method == 'GET':
            response = requests.get(_url, headers=__header, timeout=6)
        elif method == 'POST':
            response = requests.post(_url, headers=__header, data=json.dumps(data))
        elif method == 'PUT':
            if data is not None:
                response = requests.put(_url, headers=__header, data=json.dumps(data))
            else:
                response = requests.put(_url, headers=__header)
        elif method == 'DELETE':
            response = requests.delete(_url, headers=__header)
        else:
            raise Exception("[CLASHX][ERROR] unsupported method")
        return response

    def _put_base(self, endpoint, data=None):
        response = self._wrap_base(endpoint, 'PUT', data)
        if response.status_code > 300:
            if response.status_code == 503:
                raise Exception(f'An error occurred in the delay test')
            elif response.status_code == 504:
                raise TimeoutProxy()
            elif response.status_code == 404:
                raise ProxyNotFound()
            elif response.status_code == 408:
                raise ProxyDelay()
            elif response.status_code == 400:
                raise Exception(f'[CLASHX][ERROR] Format error')
            else:
                raise Exception(f'[CLASHX][ERROR] Request failed with status code {response.status_code}')
        else:
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 204:
                return {}
            else:
                return {}

    def get_conf(self) -> dict:
        return self._get_base('configs')

    def reload_conf(self) -> dict:
        return self._get_base('configs', 'PUT')

    def get_proxies(self) -> dict:
        return self._get_base('proxies')

    def get_proxy(self, name: str) -> dict:
        return self._get_base(f'proxies/{name}')

    def select_proxy_v1(self, selector_group, connection_name: str) -> bool:
        self._put_base(f'proxies/{selector_group}', {
            "name": connection_name
        })
        return True

    def test_health_proxy(self, name: str, target: str) -> dict:
        try:
            end_path = f'proxies/{name}/delay?url={target}&timeout=4000'
            response = self._wrap_base(end_path, 'GET')

            if response.status_code == 200:
                d = response.json()
                return {
                    "s": name,
                    "delay": d["delay"]
                }

            elif response.status_code == 404:
                ...
            elif response.status_code == 503:
                print(f'[CLASHX][ERROR] An error occurred in the delay test', name)
            elif response.status_code == 504:
                print(f'[CLASHX][ERROR] time out', name)
            elif response.status_code == 404:
                print(f'[CLASHX][ERROR] Proxy not found')
            elif response.status_code == 408:
                print(f'[CLASHX][ERROR] Proxy delay test timeout')
        except requests.exceptions.ReadTimeout:
            ...
        except requests.exceptions.ConnectionError:
            time.sleep(5)

        return {}

    def get_proxies_group(self) -> dict:
        return self._get_base('proxy-groups')

    def get_proxy_group(self, name) -> dict:
        return self._get_base(f'proxy-groups/{name}')

    def create_proxy_group(self, group) -> dict:
        return self._get_base('proxy-groups', 'POST', group)

    def update_proxy_group(self, name, group) -> dict:
        return self._get_base(f'proxy-groups/{name}', 'PUT', group)

    def delete_proxy_group(self, name) -> dict:
        return self._get_base(f'proxy-groups/{name}', 'DELETE')

    def get_rules(self) -> dict:
        return self._get_base('rules')

    def get_rule(self, id: str) -> dict:
        return self._get_base(f'rules/{id}')

    def create_rule(self, rule) -> dict:
        return self._get_base('rules', 'POST', rule)

    def update_rule(self, id: str, rule) -> dict:
        return self._get_base(f'rules/{id}', 'PUT', rule)

    def delete_rule(self, id: str) -> dict:
        return self._get_base(f'rules/{id}', 'DELETE')

    def get_dns(self) -> dict:
        return self._get_base('dns')

    def get_dns_provider(self, name) -> dict:
        return self._get_base(f'dns/{name}/providers')

    def get_dns_providers(self) -> dict:
        return self._get_base('dns/providers')

    def create_dns_provider(self, provider) -> dict:
        return self._get_base('dns/providers', 'POST', provider)

    def update_dns_provider(self, name, provider) -> dict:
        return self._get_base(f'dns/providers/{name}', 'PUT', provider)

    def delete_dns_provider(self, name) -> dict:
        return self._get_base(f'dns/providers/{name}', 'DELETE')
