# !/usr/bin/env python
# coding: utf-8
class GalxeMission(Exception):
    ...


class NetworkingErr(Exception):
    ...


class VPNConnectionErr(NetworkingErr):
    pass


class InternalServerErr(NetworkingErr):
    pass


class NotProperTSLClient(NetworkingErr):
    pass


class CloudFrontProtection(NetworkingErr):
    pass


class FailedToProduceCaptchaOutput(Exception):
    ...


class RequestErro(Exception):
    def __init__(self, code, content):
        print("error status code", code)
        if str(content) == "":
            print("No content is found.")
        else:
            print("error response content", str(content))


class SqlDataNotFound(GalxeMission):
    ...


class NewUser(GalxeMission):
    ...


class UriRouterNotFound(GalxeMission):
    ...


class ExpiredSignatureErr(GalxeMission):
    pass


class ReoauthFail(GalxeMission):
    ...


class GalxeIdNotCreated(GalxeMission):
    ...


class WaitForClaimPoint(GalxeMission):
    ...


class TryPerformMission(GalxeMission):
    ...


class TooManyRequest(GalxeMission):
    ...


class NetworkBusy(GalxeMission):
    ...


class MissingTwitterIdentity(GalxeMission):
    ...


class AccountRegistrationDone(GalxeMission):
    ...


class FailedToVerifyCaptcha(GalxeMission):
    ...


class RedoMission(GalxeMission):
    ...


class NoSignature(GalxeMission):
    ...


class TwitterAccountHasBeenBound(GalxeMission):
    ...


class InvalidToken(GalxeMission):
    ...


class NewEmailCodeNeeded(GalxeMission):
    ...


class WalletError(Exception):
    ...


class TokenSessionMissed(GalxeMission):
    ...


class NoReminderNote(WalletError):
    ...


class NoWalletImplemented(WalletError):
    ...


class Galxi:
    CACHE_PATH: str = "./cache"
    DOM_BASE: str = "./jslab"
    TEMP_FILE: str = "tmp.txt"
    TEMP_JS: str = "tmp.js"
    TEMP_JSON: str = "tmp.json"
    COOKIE_TMP_FILE: str = "tmp_cookie"
    HOME: str = "/root"
    KEY_FILE_FORMAT: str = "zz{COUNT_INDEX}.txt"
    FIRST_NAME_DICT: list[str] = []
    SURNAME_DICT: list[str] = []
    BEARER = ""
    ORIGIN: str = "https://....com"
    REFERER: str = "https://....com/"
    HOST: str = "...."
    GALXE_CAMPAIGN_PASSPORT: str = "...."
    FAILURE_TO_SHOW_EMAIL: int = 10
    DB_MEMBER: str = "...."
    DB_KV: str = "....."


class CashHub:
    FILTER: list[str] = [
        "此节点将在",
        "剩余",
        "DIRECT",
        "REJECT",
        "恢复",
        "节点选择",
    ]
    TEST_PROTOCOL: str = "https://.....com"
    TEST_CLASH_SELECTOR: str = "🔰 节点选择"
