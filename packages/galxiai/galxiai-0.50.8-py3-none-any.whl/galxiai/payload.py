# !/usr/bin/env python
# coding: utf-8
import time

from galxiai import ut
from galxiai.req import *
from galxiai.sqlite_galxi import GalaBox
from galxiai.const import *
import random
import json


class Structure:
    debug: bool
    db: GalaBox
    wallet_erc: any
    tasks: list = []
    email_client: any
    _geetest_mode_ai: any
    configurations: dict
    start_from_index: int

    # solution for email registrations only.
    misc_mode: bool
    serial_passes: list[str]
    pass_file_index: int
    worker_type: int


class GalStep:
    loop_index: int = 0

    def repeat_stepping(self, options: list, at_step: int = -1):
        self.loop_index -= 1
        if at_step == -1:
            t = random.choice(options)
            time.sleep(t)
        else:
            wait = options[at_step]
            print("too many request needs to slow down", wait)
            time.sleep(wait)

    def switch_account(self, x: int):
        ...

    def rack_process(self) -> int:
        ...

    def process_loop(self, loop_at: int):
        ...


class GalxiRunner(UrlReq, Structure, GalStep):

    def get_recap_response(self):
        # need to use your own custom AI captura
        return {}

    def internal_port_vpn(self, k: int):
        # self.capcha_provider.enableProxy(k)
        self.init_ai_module(k)

    def init_ai_module(self, port: int):
        ...

    def check_access_token(self, d):
        if isinstance(d, dict):
            if "signin" in d:
                Galxi.BEARER = d["signin"]
                self.db.set_jwt_token(Galxi.BEARER)

    def action_check_jwt(self):
        # check the current bearer validation
        h = rq_data_check_jwt(self.get_recap_response())
        try:
            galxeQL(self.session, h)
        except InvalidToken:
            self.action_sign_in()

    def get_passport_info(self):
        j = rq_data_passport_info(self.wallet_erc.address)
        d = galxeQL(self.session, j)
        if isinstance(d, dict):
            passport_info = d["addressInfo"]
            passport_id = passport_info["id"]
            passport = passport_info["passport"]
            if passport["status"] == "NOT_ISSUED":
                print("need to issue passport")
            else:
                print(passport)

    def get_passport_camp_info(self):
        j = rq_data_get_campaign_info(self.wallet_erc.address, Galxi.GALXE_CAMPAIGN_PASSPORT)
        d = galxeQL(self.session, j)
        if "campaign" in d:
            if d["campaign"]["status"] != "Active":
                print("passport campaign is closed. maybe")
        else:
            print(d)

    def action_call_add_cred(self, cred_it: str, camp_id: str):
        d = None
        try:
            g = rq_data_add_cred(cred_it, self.wallet_erc.address, self.get_recap_response())
            d = galxeQL(self.session, g)
        except FailedToVerifyCaptcha:
            time.sleep(60)
            self.log_failed_verifications()
            self.action_call_add_cred(cred_it, camp_id)
            return

        if isinstance(d, dict):
            self.db.check_point_synced(cred_it)
            self.db.check_point_claim(cred_it)

    def action_claim_points(self, camp_id: str):
        # if self.db.is_check_point_cp_ready(camp_id) is False:
        #    print("claim campaign check point not ready.")
        #    return
        d = None
        try:
            d = galxeQL(self.session, rq_data_claim_points(camp_id, self.wallet_erc.address, self.get_recap_response()))
        except FailedToVerifyCaptcha:
            time.sleep(60)
            self.log_failed_verifications()
            self.action_claim_points(camp_id)
            return
        print("==== claim progress points")
        if isinstance(d, dict):
            if d["prepareParticipate"]["allow"] is True:
                claim_points = d["prepareParticipate"]["loyaltyPointsTxResp"]["TotalClaimedPoints"]
                print(f"Claim points {claim_points}")
                self.db.check_point_campaign(camp_id)
                self.db.update_res_kv(camp_id, True)
            else:
                reason = str(d["prepareParticipate"]["disallowReason"]).lower()
                if "exceed limit" in reason:
                    self.db.update_res_kv(camp_id, True)
                if "empty reward" in reason:
                    self.db.update_res_kv(camp_id, True)

    def action_claim_pt_once(self, camp_id: str):
        if self.db.get_key_res("hasEmail") is False:
            return
        if self.db.has_res_key(camp_id) is True:
            return
        print("====== claim solana point")
        d = galxeQL(self.session, rq_data_campaign_detail(self.wallet_erc.address, camp_id, True))
        if "campaign" in d:
            if "whitelistInfo" in d["campaign"]:
                info = d["campaign"]["whitelistInfo"]
                if info["claimedLoyaltyPoints"] > 0:
                    self.db.update_res_kv(camp_id, True)
                    print("point claimed")
                else:
                    self.claim_that(camp_id)

    def claim_that(self, camp_id):
        d = galxeQL(self.session, rq_data_claim_points(camp_id, self.wallet_erc.address, self.get_recap_response()))
        if isinstance(d, dict):
            if d["prepareParticipate"]["allow"] is True:
                claim_points = d["prepareParticipate"]["loyaltyPointsTxResp"]["TotalClaimedPoints"]
                print(f"Claim Points {claim_points}")
                self.db.update_res_kv(camp_id, True)
            else:
                reason = str(d["prepareParticipate"]["disallowReason"]).lower()
                print(reason)
                if "exceed limit" in reason:
                    self.db.update_res_kv(camp_id, True)
                if "empty reward" in reason:
                    self.db.update_res_kv(camp_id, True)

        else:
            print("error from claim progress once")

    def action_perform_camp(self, camp_id: str):
        d = galxeQL(self.session, rq_data_campaign_detail(self.wallet_erc.address, camp_id, False))
        call_to_actions = []
        if isinstance(d, dict):
            credential_gp = d["campaign"]["credentialGroups"]
            for h in credential_gp:
                if "credentials" in h:
                    f = h["credentials"]
                    if len(f) > 0:
                        action_call = f[0]
                        do_url = action_call["referenceLink"]
                        cred_it = action_call["id"]
                        sync = action_call["lastSync"]
                        if self.check_perform_action(camp_id, cred_it, do_url, sync):
                            print("do task", cred_it, do_url)
                            call_to_actions.append((
                                cred_it, do_url
                            ))
                            self.action_call_add_cred(cred_it, camp_id)
        self.tasks = call_to_actions

    def check_perform_action(self, camp_id, cred_id, do_url, sync) -> bool:
        return self.db.is_check_point_ready(cred_id) is True or sync == 0

    def action_check_credentials(self):
        if len(self.tasks) == 0:
            return
        for task_mission in self.tasks:
            (cred_id, url) = task_mission
            if self.db.check_claim_ready(cred_id) is False:
                raise WaitForClaimPoint()
            d = galxeQL(self.session, rq_data_sync_cred(cred_id, self.wallet_erc.address))
            if "syncCredentialValue" not in d:
                print("error from not able to receive..")
                continue
            contains = d["syncCredentialValue"]
            if "message" in contains:
                msg = str(contains["message"]).lower()
                if "please click the go button and visit the link first. then try again in" in msg:
                    print("check result too fast..")
                    if self.db.is_task_just_done(cred_id) is True:
                        self.db.check_point_claim(cred_id)
                        raise TryPerformMission()
                else:
                    if msg != "none":
                        print(msg)
            if "value" in contains:
                action_result = contains["value"]["allow"]
                if action_result is True:
                    print(f"Check credit for {cred_id} - completed")
        # self.action_claim_points(Galxi.IO_NET_CAMPAIGN_1)

    def action_get_api_token(self):
        if self.db.has_res_key("api_key") is True:
            return
        _doc = galxeQL(self.session, rq_data_update_access_token(self.wallet_erc.address))
        if "updateAccessToken" in _doc:
            self.db.update_res_kv("api_key", _doc["updateAccessToken"]["accessToken"])

    def action_twitter_action_post_twitter(self, text: str):

        return ""

    def twitter_verification_message(self):
        user_id = self.db.get_key_res("id")
        return f"Verifying my Twitter account for my #GalxeID gid:{user_id} @Galxe"

    def action_twitter_ac_bind(self):
        if self.db.res_true("hasTwitter") is True:
            print("twitter ac bound.")
            return

        print("============= confirm twitter ac")
        url = self.action_twitter_action_post_twitter(self.twitter_verification_message())
        _doc = galxeQL(self.session, rq_data_fill_twitter_ac(self.wallet_erc.address, url))
        if "twitterUserID" in _doc and "twitterUserName" in _doc:
            print(".ok 1")
        _doc = galxeQL(self.session, rq_data_twitter_verify(self.wallet_erc.address, url))
        if "twitterUserID" in _doc and "twitterUserName" in _doc:
            print(".ok 2")
            
        print("twitter is just ac bound.")
        self.action_get_profile()

    def action_email_confirm(self):
        print("============= confirm email")
        _doc = None

        if self.db.is_email_sent() is False:
            print("no email has been sent")
            return

        if self.db.is_email_sent_reset() is True:
            print("resend email is needed")
            return

        if self.db.is_email_sent_expired() is True:
            print("email has been sent over one hour")
            return
        pend_email = self.db.get_key_res("pending_email")
        mail_id = self.db.get_key_res("temp_email_code")
        if pend_email == "" or mail_id == "":
            print("empty email code or email")
            return
        print(f"found pending email: {pend_email}")
        self.action_sign_in()
        ver_code = self.email_client.loop_z(mail_id, pend_email, "galxe")
        _doc = galxeQL(self.session, rq_data_email_verification(pend_email, self.wallet_erc.address, ver_code))
        if isinstance(_doc, dict):
            if "updateEmail" in _doc:
                self.db.update_res_kv("email_code", ver_code)
                print("bound email address SUCCESS")

    def action_email_binding(self):
        self.action_get_profile()
        _doc = None
        print("============= bind email")
        if self.db.res_true("hasEmail") is False:
            if self.db.is_email_sent() is True and self.db.is_email_sent_expired() is False:
                print("just send out the email now needs to check the email")
                return
            while True:
                (use_email, mail_id) = self.email_client.get_email_address()
                try:
                    _doc = galxeQL(self.session, rq_data_email_registration(
                        use_email, self.wallet_erc.address, self.get_recap_response()))

                except FailedToVerifyCaptcha:
                    print("captcha retry for new_email_code, try again in 60s")
                    time.sleep(60)
                    self.log_failed_verifications()
                    continue

                except RequestErro:
                    print("request error")
                    continue

                if isinstance(_doc, dict) is False:
                    print("result is failure.")
                    continue

                if "sendVerificationCode" in _doc:
                    self.db.update_res_kv("temp_email_code", mail_id)
                    self.db.update_res_kv("pending_email", use_email)
                    self.db.checked_email_send_time()
                    print("confirmation email is sent to", use_email)
                    break
        else:
            print("email is bound")
            self.loop_index = 20

    def get_new_user_nickname(self) -> str:
        return ""

    def action_register_username(self):
        self.action_get_profile()
        if self.db.get_key_res("username") == "":
            _name = ""
            while True:
                _name = self.get_new_user_nickname()
                d = galxeQL(self.session, rq_data_username_check(_name))
                if isinstance(d, dict):
                    if d["usernameExist"] is False:
                        break

            d = galxeQL(self.session, rq_data_create(_name, self.wallet_erc.address))
            if "createNewAccount" in d:
                self.db.update_res_kv("id", d["createNewAccount"])
                self.action_get_profile()

    def action_sign_in(self):
        m, sign = self.wallet_erc.sign_galxe_msg()
        _doc = galxeQL(self.session, rq_data_galxe_sign_in(m, sign, self.wallet_erc.address))
        self.check_access_token(_doc)

    def action_update_token(self):
        _doc = galxeQL(self.session, rq_data_update_access_token(self.wallet_erc.address))
        self.check_access_token(_doc)

    def action_init(self):
        found_address_rec = self.db.has_the_address(self.wallet_erc.address)
        bearer_x = self.db.get_access_token() if found_address_rec is True else ""
        if found_address_rec is False or bearer_x == "":
            self.action_sign_in()
            self.action_register_username()
            _doc = galxeQL(self.session, rq_data_galxe_id(self.wallet_erc.address))
            if _doc["galxeIdExist"] is False:
                print("galxe id is not exist.")
        else:
            Galxi.BEARER = bearer_x
            self.action_check_jwt()
        self.action_register_username()

    def log_failed_verifications(self):
        self.db.log_failed_verifications()

    def profile_res_check(self, _d):
        try:
            _info = _d["addressInfo"]
            data = {
                "id": _info["id"],
            }

            ut.check_kv_or_update(data, _info, "id")
            ut.check_kv_or_update(data, _info, "username")
            ut.check_kv_or_update(data, _info, "address")
            ut.check_kv_or_update(data, _info, "hasEmail")
            ut.check_kv_or_update(data, _info, "solanaAddress")
            ut.check_kv_or_update(data, _info, "seiAddress")
            ut.check_kv_or_update(data, _info, "bitcoinAddress")
            ut.check_kv_or_update(data, _info, "twitterUserID")
            ut.check_kv_or_update(data, _info, "twitterUserName")
            ut.check_kv_or_update(data, _info, "email")
            ut.check_kv_or_update(data, _info, "displayNamePref")
            ut.check_kv_or_update(data, _info, "hasWorldcoin")
            ut.check_kv_or_update(data, _info, "hasWorldcoin")
            self.db.update_res_set(data)
            print("profile updated.")
        except ValueError:
            print(_d)

    def action_get_profile(self):
        d = galxeQL(self.session, rq_data_get_profile(self.wallet_erc.address))
        self.profile_res_check(d)

    def create_new_account(self, user_name: str):
        d = galxeQL(self.session, rq_data_create(self.wallet_erc.address, user_name))
        self.db.update_res_kv("id", d["createNewAccount"])
