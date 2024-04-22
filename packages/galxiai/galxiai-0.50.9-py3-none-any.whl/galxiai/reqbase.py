from galxiai.xxcl import CashCat
import os
try:
    import tls_client
except:
    os.system('python -m pip install tls-client')
    import tls_client


class BaseReClient:
    session: tls_client.Session
    proxy_agent: CashCat
    agent_x: str
    cookie_use: bool
    _port_vpn: int
    _retry_failure_connection: int = 0

    def handle_limited_ip(self):
        self._retry_failure_connection += 1
        if self.on_vpn() is False:
            if self._retry_failure_connection > 2:
                self._retry_failure_connection = 0
                self.failure_in_connection_try_proxy()
                return False
            return False
        else:
            if self._retry_failure_connection > 2:
                self.proxy_agent.rotate_conn()
                self._retry_failure_connection = 0
                return True
            return False

    @property
    def at_connection_fails(self):
        return self._retry_failure_connection

    # https://amiunique.org/fingerprint
    def urlreq__init__(self, conf: dict):
        self.agent_x = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0"
        self.reset_client()
        self._retry_failure_connection = 0
        self.cookie_use = False
        use_clash = False
        if use_clash:
            self.proxy_agent = CashCat()
            self.proxy_agent.install_conf(conf)
            self.proxy_agent.test_protocol()

    def failure_in_connection_try_proxy(self):
        print("now try using proxy")
        self.port_vpn = 7890
        self.proxy_agent.setup()

    def reset_client(self):
        self.agent_x = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0"
        self.session = tls_client.Session(
            client_identifier="firefox_120",
            supported_signature_algorithms=[
                "ECDSAWithSHA256",
                "SHA256",
                "SHA384",
                "SHA512",
                "SHA256WithRSAEncryption",
                "SHA384WithRSAEncryption",
                "SHA512WithRSAEncryption",
                "ECDSAWithSHA384"
            ],
            supported_versions=["GREASE", "1.3", "1.2"],
            key_share_curves=["GREASE", "X25519"],
            cert_compression_algo="brotli",
            pseudo_header_order=[
                ":method",
                ":authority",
                ":scheme",
                ":path"
            ],
            connection_flow=15663107,
            header_order=[
                "user-agent",
                "accept",
                "accept-encoding",
                "accept-language",
            ]
        )

    def on_vpn(self) -> bool:
        return self._port_vpn > 0

    @property
    def port_vpn(self) -> int:
        """I'm the 'x' property."""
        return self._port_vpn

    @port_vpn.setter
    def port_vpn(self, value: int):
        self._port_vpn = value
        if value > 0:
            self.session.proxies = {
                'http': f'http://127.0.0.1:{value}',
                'https': f'http://127.0.0.1:{value}'
            }
        else:
            self.session.proxies = None
        self.internal_port_vpn(value)

    def internal_port_vpn(self, k: int):
        pass
