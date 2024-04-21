# !/usr/bin/env python
# coding: utf-8
import datetime
import uuid
from galxiai.const import *
from galxiai.ql import *
import os
import json

from galxiai.reqbase import BaseReClient
from galxiai.ut import json_save

try:
    import tls_client
except:
    os.system('python -m pip install tls-client')
    import tls_client


def rq_data_address_info(first: int = 30):
    return {
        "query": SPACESINADDRESSINFO,
        "variables": {
            "address": "",
            "listSpaceInput": {"first": first},
            "operationName": "SpacesInAddressInfo",
        }
    }


def rq_data_passport_info(var_address: str):
    return {
        "query": PASSPORTINFO,
        "variables": {
            "address": var_address
        }
    }


def rq_data_check_jwt(_captcha: dict):
    return {
        "query": CHECK_JWT_QL,
        "variables": {
            "captchaInput": _captcha,
            "operationName": "CheckJWT",
        }
    }


def rq_data_campaign_detail(address: str, campaign_id: str, with_address: bool):
    return {
        "query": CAMPAIGNDETAILALL,
        "operationName": "CampaignDetailAll",
        "variables": {
            "address": address.lower(),
            "id": campaign_id,
            "withAddress": with_address
        }
    }


def rq_data_get_profile(address: str):
    return {
        "query": PROFILEQ,
        "operationName": "BasicUserInfo",
        "variables": {
            "address": address
        },
    }


def rq_data_get_campaign_info(address: str, camp_id: str):
    return {
        "query": GET_CAMP_INFO,
        "operationName": "CampaignInfo",
        "variables": {
            "address": address,
            "id": camp_id
        },
    }


def rq_data_issue_persona_kyc_id(address: str, signature: str):
    return {
        "query": CREATE_PERSONA_ID,
        "operationName": "GetOrCreateInquiryByAddress",
        "variables": {
            "input": {
                "address": address,
                "signature": signature
            }
        },
    }


def rq_data_get_plus_expire(address: str):
    return {
        "query": PROFILEQ,
        "operationName": "GetGalaxyPlusExpire",
        "variables": {
            "galxeId": address
        },
    }


def rq_data_username_check(name: str):
    return {
        "query": CHECKUSERNAME,
        "operationName": "IsUsernameExisting",
        "variables": {
            "username": name
        }
    }


def rq_data_create(name: str, address_evm: str):
    return {
        "query": CREATENEWACCOUT,
        "operationName": "CreateNewAccount",
        "variables": {
            "input": {
                "username": name,
                "socialUsername": "",
                "schema": f"EVM:{address_evm}",
            }
        }
    }


def rq_data_space_loyalty_pt(address: str):
    return {
        "query": SPACELOYALTYPT,
        "operationName": "SpaceLoyaltyPoints",
        "variables": {
            "id": "46841",
            "address": address
        },
    }


def rq_data_galxe_sign_in(msg: str, signature: str, address: str):
    return {
        "operationName": "SignIn",
        "variables": {
            "input": {
                "address": address,
                "message": msg,
                "signature": signature,
                "addressType": "EVM",
                "publicKey": ""
            }
        },
        "query": SIGNIN
    }


def rq_data_galxe_id(address_evm: str):
    return {
        "query": GALXEIDEXIST,
        "operationName": "GalxeIDExist",
        "variables": {
            "schema": f"EVM:{address_evm}"
        }
    }


def rq_data_update_access_token(address_evm: str):
    return {
        "query": UPDATEACCESSTOKEN,
        "operationName": "UpdateAccessToken",
        "variables": {
            "input": {
                "address": address_evm
            }
        }
    }


def rq_data_email_registration(_email_address: str, _address: str, _captcha: dict):
    return {
        "query": EMAIL_X,
        "operationName": "SendVerifyCode",
        "variables": {
            "input": {
                "address": _address.lower(),
                "captcha": _captcha,
                "email": _email_address
            }
        }
    }


def rq_data_email_verification(_email: str, _address: str, verification_code: str):
    return {
        "query": EMAIL_UPDATE_VERIF,
        "operationName": "UpdateEmail",
        "variables": {
            "input": {
                "address": _address.lower(),
                "email": _email,
                "verificationCode": verification_code
            }
        }
    }


def rq_data_get_whitelist_sites():
    return {
        "query": GETWHITELISTSITES,
        "operationName": "getWhitelistSites"
    }


def rq_data_recommended_campaign_by_user(recommendByCampaignId: str):
    return {
        "query": RECOMMENDCAMPAIGN,
        "variables": {
            "input": {
                "after": "-1",
                "first": 12,
                "recommendByCampaignId": recommendByCampaignId,
                "recommendByUser": ""
            }
        },
        "operationName": "getMessageStatus"
    }


def rq_data_spaces_by_campaign_user(camp_id: str):
    return {
        "operationName": "RecommendSpacesByCampiagnAndUser",
        "variables": {
            "input": {
                "recommendByUser": "",
                "recommendByCampaignId": camp_id,
                "first": 4,
                "after": "-1"
            },
            "spaceCampaignsInput": {
                "statuses": [
                    "Active"
                ]
            }
        },
        "query": RECOMMENDSPACESBYCAMPIAGNUSER
    }


def rq_data_add_cred(cred_it: str, address: str, captcha: dict):
    return {
        "operationName": "AddTypedCredentialItems",
        "variables": {
            "input": {
                "credId": cred_it,
                "operation": "APPEND",
                "items": [
                    address
                ],
                "captcha": captcha,
            }
        },
        "query": ADDCRED
    }


def rq_data_cred_fill_content(cred_it: str, _address: str, content: str):
    return {
        "operationName": "SyncCredentialValue",
        "variables": {
            "input": {
                "syncOptions": {
                    "credId": cred_it,
                    "address": _address,
                    "survey": {
                        "answers": [
                            content
                        ]
                    }
                }
            }
        },
        "query": SYNCCREDVAL
    }


def rq_data_claim_points(camp_id: str, evm_address: str, _captcha: dict):
    return {
        "operationName": "PrepareParticipate",
        "variables": {
            "input": {
                "signature": "",
                "campaignID": camp_id,
                "address": evm_address,
                "mintCount": 1,
                "captcha": _captcha,
                "chain": "ETHEREUM",
            }
        },
        "query": PREPAREPARTICIPATE
    }


def rq_data_sync_cred(cred_it: str, address: str):
    return {
        "operationName": "SyncCredentialValue",
        "variables": {
            "input": {
                "syncOptions": {
                    "credId": cred_it,
                    "address": address
                }
            }
        },
        "query": SYNC_CRED
    }


def rq_data_campaign_participants(campId: str):
    return {
        "query": CAMPAIGNPARTICIPANTS,
        "variables": {
            "pDownload": False,
            "bDownload": False,
            "isParent": False,
            "id": campId,
            "pfirst": 10,
            "pafter": "-1",
            "wfirst": 10,
            "wafter": "-1"
        },
        "operationName": "campaignParticipants"
    }


def ge_header(html_request: bool = False):
    basic = {
        'Host': Galxi.HOST,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0'
    }
    if html_request is False:
        basic.update({
            'Content-Type': 'application/json',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Origin': Galxi.ORIGIN,
            'Referer': Galxi.REFERER
        })
    else:
        basic.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Upgrade-Insecure-Requests': '1',
        })

    if Galxi.BEARER != "":
        basic.update({
            "authorization": Galxi.BEARER
        })

    basic.update({
        "request-id": str(uuid.uuid1()),
        "TE": "trailers",
    })

    return basic


def post_doc_header():
    h = ge_header(html_request=True)
    h.update({
        "Origin": Galxi.ORIGIN,
        "Content-Type": "application/x-www-form-urlencoded",
        "TE": "trailers",
    })
    return h


def galxeQL(session: tls_client.Session, rq_data: dict):
    p = session.post("https://graphigo.prd.galaxy.eco/query", json=rq_data, headers=ge_header())
    return handle_gl_resource(p)


class UrlReq(BaseReClient):
    def useManualCookie(self):
        self.cookie_use = True


def handle_gl_resource(r):
    plain_text = str(r.text).lower()
    if "not found" in plain_text:
        raise UriRouterNotFound()
    if "generated by cloudfront" in plain_text:
        raise NetworkBusy()
    if "ai server is busy" in plain_text:
        print(plain_text)
        raise TooManyRequest()
    if "no users signed in" in plain_text:
        raise NewUser()
    if r.status_code == 504:
        raise TimeoutError()
    if r.status_code == 422:
        raise RequestErro(
            r.status_code,
            "probably missing input values or some sort, go back and double check the requesting json."
        )
    if r.status_code == 403:
        print(r.status_code)
        print(r.content)
        return False
    if r.status_code == 429:
        print("too many request")
        raise TooManyRequest()
    if r.status_code == 503:
        raise TooManyRequest()
    if r.status_code == 500:
        raise InternalServerErr()
    if r.status_code > 200:
        try:
            f = r.json()
            if "errors" in f:
                msg = str(f["errors"][0]["message"]).lower()
                if "failed to verify recaptcha" in msg:
                    raise FailedToVerifyCaptcha()
                raise RequestErro(r.status_code, msg)
        except json.decoder.JSONDecodeError:
            print("no json")
        raise RequestErro(r.status_code, r.content)

    f = r.json()
    if "errors" in f:
        msg = str(f["errors"][0]["message"]).lower()
        t = datetime.datetime.now()
        msg = f"{msg}, {str(t)}"
        if "failed to verify recaptcha" in msg:
            print(msg)
            raise FailedToVerifyCaptcha()
        elif "internal desc = fail to verify recaptcha" in msg:
            print(msg)
            raise FailedToVerifyCaptcha()
        elif "malformed survey cred value" in msg:
            raise TooManyRequest()
        elif "expired signature" in msg:
            raise ExpiredSignatureErr()
        elif "problem with the service. please try again later" in msg:
            raise TooManyRequest()
        elif "please create galxe id" in msg:
            raise GalxeIdNotCreated()
        elif "wrong code, please try again" in msg:
            raise NewEmailCodeNeeded()
        elif "fail to get verification code" in msg:
            raise NewEmailCodeNeeded()
        elif "invalid jwt token" in msg:
            raise InvalidToken()
        else:
            t = datetime.datetime.now()
            msg = f"{msg}, {str(t)}"
            raise RequestErro(r.status_code, msg)
    if "data" in f:
        json_save(r.content)
        return f["data"]
