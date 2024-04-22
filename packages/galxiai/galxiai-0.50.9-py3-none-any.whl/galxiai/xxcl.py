import datetime
import json
import os
import time
from typing import Tuple, Union

from galxiai.const import *
from galxiai.clasreq import ClashAPI, APIBase, ProxyNotFound
from concurrent.futures import ThreadPoolExecutor, as_completed


class CashCat(ClashAPI, APIBase):
    """
    use clash api to connect to the working clash api hub
    """

    def __init__(self):
        super().__init__()
        self._ps = []
        self.available = []
        self.sock = "socks5://127.0.0.1:{}"
        self.httpproxy = "http://127.0.0.1:{}"
        self.mixport = 0
        self.work = False
        self.loaded = False
        self.health = 0
        self.vpn_iter_n = 0
        self.error_count = 0
        self._status = 0

    def setup(self):
        self.conf = self.get_conf()
        proxies = self.get_proxies()
        list_proxy = proxies["proxies"]["GLOBAL"]
        print(list_proxy)

    def install_conf(self, configuration: dict) -> "CashCat":
        if 'clash_proxy' not in configuration:
            print("no clash setting in the configuration file.")
            return self

        clash_pro = configuration['clash_proxy']

        if 'secret' in clash_pro:
            print("use secret", clash_pro['secret'])
            self.secret_bearer = clash_pro['secret']

        if 'conn_file' in clash_pro:
            print("read connect path", clash_pro['conn_file'])
            self.read_connection_file(clash_pro['conn_file'])

        if 'selector' in clash_pro:
            print("read selector", clash_pro['selector'])
            CashHub.TEST_CLASH_SELECTOR = clash_pro['selector']

        if 'test_endpoint' in clash_pro:
            print("read test endpoint", clash_pro['test_endpoint'])
            CashHub.TEST_PROTOCOL = clash_pro['test_endpoint']

        return self

    def check_unuse_name(self, connection_name: str):
        for key in CashHub.FILTER:
            if key in connection_name:
                return True
        return False

    def in_thread_scan(self):
        self.available = []
        proxies = self.get_proxies()
        self._ps = proxies["proxies"]["GLOBAL"]["all"]
        for pname in self._ps:
            if self.check_unuse_name(pname):
                continue
            self.available.append({
                "s": pname,
                "delay": 0
            })
        workers = len(self.available)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_rs = [executor.submit(self.test_health_proxy, proxy_name['s'], CashHub.TEST_PROTOCOL) for
                         proxy_name in self.available]
            for future in as_completed(future_rs):
                result = future.result()
                if isinstance(result, dict):
                    if result != {}:
                        self.update_delay(result)

    def scan(self):
        self.test_protocol()
        self.conf = self.get_conf()
        self.mixport = self.conf["mixed-port"]
        while True:
            r = datetime.datetime.now()
            self.in_thread_scan()
            print("------", r)
            time.sleep(3)

    def update_delay(self, result: dict):
        updated = False
        for v in self.available:
            if v["s"] == result["s"]:
                v.update({
                    "delay": result["delay"]
                })
                updated = True
                break
        if updated is False:
            return
        base_database = os.path.join(CashHub.CACHE_PATH, "proxy_config.json")
        print("update", result["s"])
        with open(base_database, 'w') as file:
            file.write(json.dumps(self.available, indent=2))
            file.close()

    def rotate_conn(self):
        self.work = False
        while True:
            self._read_connections()
            self.vpn_iter_n += 1
            self._status = 1
            res = self._double_check()
            if res is True or self.work is True:
                break

    @property
    def proxyendpoint(self) -> Union[str, None]:
        if self.work:
            return self.httpproxy.format(self.mixport)
        else:
            return None

    @property
    def now_n(self) -> int:
        return self.vpn_iter_n % len(self.available)

    @property
    def connection(self) -> str:
        return self.available[self.now_n]["s"]

    @property
    def delay(self) -> int:
        return int(self.available[self.now_n]["delay"])

    @delay.setter
    def delay(self, n: int):
        self.available[self.now_n]["delay"] = n

    def _test_current_connect(self):
        try:
            self._status = 1
            _fs = self.test_health_proxy(self.connection, CashHub.TEST_PROTOCOL)
            self.delay = int(_fs["delay"])
            return True
        except Exception as e:
            self.delay = -1
            return False
        # self.update_delay(self.available[self.now_n])

    def _double_check(self):
        if 0 < self.delay < 3000:
            try:
                if self._test_current_connect() and 0 < self.delay < 3000:
                    self.work = self.select_proxy_v1(CashHub.TEST_CLASH_SELECTOR, self.connection)
                    print(f"connected to {self.connection} OK")
                    return True
                else:
                    return False
            except ProxyNotFound:
                print("ProxyNotFound")
                time.sleep(10)
                return False
        else:
            return False
