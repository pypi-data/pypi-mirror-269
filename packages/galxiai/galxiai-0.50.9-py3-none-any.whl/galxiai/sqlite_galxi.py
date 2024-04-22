# !/usr/bin/env python
# coding: utf-8
import datetime
import math
import sqlite3
import uuid

from SQLiteAsJSON import ManageDB
from SQLiteAsJSON.SQLiteAsJSON import db_logger
import os.path
import json
import random
from requests import Response
import jwt
from typing import Tuple, Union
from galxiai.const import *
from galxiai.ut import obj_to_tuple, obj_to_string


class DB_Fields:
    member_id: str
    user_addr: str
    has_update_time: bool = False


class MemberMgm(ManageDB, DB_Fields):
    """
    modified blockchain db controller
    """

    def total_count(self, tbl: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) as count FROM {tbl}")
        (count,) = cursor.fetchone()
        cursor.close()
        if count > 0:
            print(count)
        return count

    def found_table(self, tableName: str) -> bool:
        sqlStatement = f"SELECT name FROM sqlite_sequence WHERE type='table' AND name='{tableName}'"
        cursor = self.conn.cursor()
        cursor.execute(sqlStatement)
        db_result = cursor.fetchone()
        cursor.close()
        if db_result is None:
            return False
        else:
            return True

    def has_address(self, tbl: str, address_key: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT address_evm FROM {tbl} WHERE address_evm = ?", (address_key,))
        db_result = cursor.fetchone()
        cursor.close()
        if db_result is None:
            return False
        else:
            return True

    def has_the_timestamp(self, tbl: str, k: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {tbl} WHERE reg_time = ?", (k,))
        db_result = cursor.fetchone()
        cursor.close()
        if db_result is None:
            return False
        else:
            return True

    def has_row(self, tbl: str, member_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {tbl} WHERE member_id = ?", (member_id,))
        db_result = cursor.fetchone()
        cursor.close()
        if db_result is None:
            return False
        else:
            return True

    def update_col_unsafe(self, tbl: str, address_key: str, params: dict) -> bool:
        if address_key[0:2] != "0x":
            return False

        try:
            columns = obj_to_string(params)
            # update query
            self.conn.execute(f"UPDATE {tbl} set {columns} WHERE address_evm='{address_key}'")
        except sqlite3.OperationalError:
            return False
        except Exception as E:
            db_logger.error('Data Update Error : ', E)
            return False
        self.conn.commit()
        return True

    def update_col_unsafe_by_member_id(self, tbl: str, member_id: str, params: dict) -> bool:
        try:
            columns = obj_to_string(params)
            # update query
            self.conn.execute(f"UPDATE {tbl} set {columns} WHERE member_id='{member_id}'")
        except sqlite3.OperationalError:
            return False
        except Exception as E:
            db_logger.error('Data Update Error : ', E)
            return False
        self.conn.commit()
        return True

    def insert_simple_row(self, tbl: str, params: dict) -> bool:
        # params["timestamp"] = round(time.time() * 1000)  # Current unix time in milliseconds
        keys, vals = obj_to_tuple(params)
        # insert query
        try:
            query = (
                f'INSERT INTO {tbl} ({keys}) VALUES ({vals})'
            )
            self.conn.execute(query, params)
            self.conn.commit()
        except (
                sqlite3.OperationalError,
                Exception
        ) as e:
            db_logger.error('Data Insert Error : ', e)
            return False
        return True

    def get_member_res(self, tbl: str, address_key: str) -> dict:
        cursor = self.conn.cursor()
        _da = {}
        res_01 = None
        try:
            cursor.execute(f'SELECT member_id, next_action, res FROM {tbl} WHERE address_evm = ?',
                           (address_key,))
            (tx_id, next_d, res_01) = cursor.fetchone()
        except Exception as E:
            db_logger.error('Data Insert Error : ', E)
        cursor.close()
        _da = json.loads(res_01)
        return _da

    def get_member_id(self, tbl: str, address_key: str) -> str:
        cursor = self.conn.cursor()
        _da = {}
        tx_id = ''
        try:
            cursor.execute(f'SELECT member_id, next_action FROM {tbl} WHERE address_evm = ?',
                           (address_key,))
            (tx_id, next_d) = cursor.fetchone()
        except Exception as E:
            db_logger.error('Data Insert Error : ', E)
        cursor.close()
        return tx_id

    def get_ref_code_ids(self, tbl: str, address_key: str) -> Tuple[str, str]:
        cursor = self.conn.cursor()
        _da = {}
        referral_code = ''
        parent_code = ''
        try:
            cursor.execute(f'SELECT member_id,referral_code, parent_code FROM {tbl} WHERE address_evm = ?',
                           (address_key,))
            (tx_id, referral_code, parent_code) = cursor.fetchone()
        except Exception as E:
            db_logger.error('Data Insert Error : ', E)
        cursor.close()
        return referral_code, parent_code

    def get_member_res_from_id(self, tbl: str, user_id: str) -> dict:
        cursor = self.conn.cursor()
        _da = {}
        res_01 = None
        try:
            cursor.execute(f'SELECT member_id, next_action, res FROM {tbl} WHERE member_id = ?',
                           (user_id,))
            (tx_id, next_d, res_01) = cursor.fetchone()
        except Exception as E:
            db_logger.error('Data Insert Error : ', E)
        cursor.close()
        _da = json.loads(res_01)
        return _da

    def get_next_action(self, tbl: str, address_key: str) -> dict:
        cursor = self.conn.cursor()
        _da = {}
        next_action = None
        try:
            cursor.execute(f'SELECT member_id, next_action FROM {tbl} WHERE address_evm = ?',
                           (address_key,))
            (tx_id, next_action) = cursor.fetchone()
            _da = json.loads(next_action)
        except json.JSONDecodeError as e:
            db_logger.error('Its ok now', e)
        except Exception as E:
            db_logger.error('Data Insert Error : ', E)
        cursor.close()
        return _da

    def get_next_action_by_id(self, tbl: str, member_id: str) -> dict:
        cursor = self.conn.cursor()
        _da = {}
        next_action = None
        try:
            cursor.execute(f'SELECT member_id, next_action FROM {tbl} WHERE member_id = ?',
                           (member_id,))
            (tx_id, next_action) = cursor.fetchone()

            _da = json.loads(next_action)
        except json.JSONDecodeError as e:
            db_logger.error('Its ok now', e)
        except Exception as E:
            db_logger.error('Data Insert Error : ', E)
        cursor.close()
        return _da

    def get_raw_json_profile(self, tbl: str, address_key: str) -> dict:
        cursor = self.conn.cursor()
        _da = {}
        profile = None
        try:
            cursor.execute(f'SELECT address_evm, profile FROM {tbl} WHERE address_evm = ?',
                           (address_key,))
            (tx_id, profile) = cursor.fetchone()
            _da = json.loads(profile)
        except Exception as E:
            db_logger.error('Data Insert Error : ', E)
        cursor.close()

        return _da

    def _is_what_ready_res(self, tble_member: str, address: str, key: str, default_flag: bool) -> bool:
        if self.has_address(tble_member, address) is False:
            return False
        from_dat = self.get_next_action(tble_member, address)
        if key in from_dat:
            time_next = from_dat[key]
            return self.get_time_now() > time_next
        print(f"key {key} not exist. decision is OK.")
        return default_flag

    def _is_what_delta(self, tble_member: str, address: str, key: str, default_value: int) -> int:
        if self.has_address(tble_member, address) is False:
            return default_value
        from_dat = self.get_next_action(tble_member, address)
        if key in from_dat:
            time_next = from_dat[key]
            return self.get_time_now() - time_next
        return default_value

    def _is_time_exists(self, tble_member: str, address: str, key: str) -> bool:
        if self.has_address(tble_member, address) is False:
            return False
        from_dat = self.get_next_action(tble_member, address)
        return key in from_dat

    def _check_point_is_zero(self, tble_member: str, address: str, key: str) -> bool:
        # if the email is sent
        if self.has_address(tble_member, address) is False:
            return False
        from_dat = self.get_next_action(tble_member, address)
        if key not in from_dat:
            return False
        value = from_dat[key]
        return value == 0

    def _check_point_recently(self, tble_member: str, address: str, key: str) -> bool:
        # if the email is sent
        if self.has_address(tble_member, address) is False:
            return False
        from_dat = self.get_next_action(tble_member, address)
        if key not in from_dat:
            return False
        value = from_dat[key]
        return value > 0

    def get_time_now(self, future_seconds: int = 0) -> int:
        current_time = datetime.datetime.now().timestamp()
        current_time = int(current_time) + future_seconds
        return current_time

    def get_mem_update_time(self, address: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT update_time FROM {Galxi.DB_MEMBER} WHERE address_evm = ?", (address,))
        (update_time,) = cursor.fetchone()
        cursor.close()
        return update_time

    def _check_point_update_res(self, tble_member: str, address: str, key: str, next_seconds: int = 3600):
        from_dat = self.get_next_action(tble_member, address)
        from_dat.update({
            key: self.get_time_now(next_seconds)
        })
        self.update_col_unsafe(tble_member, address, {
            "next_action": json.dumps(from_dat)
        })

    def _check_point_zero(self, tble_member: str, address: str, key: str):
        from_dat = self.get_next_action(tble_member, address)
        from_dat.update({
            key: 0
        })
        self.update_col_unsafe(tble_member, address, {
            "next_action": json.dumps(from_dat)
        })

    def get_first_row(self, tbl: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT member_id FROM {tbl}")
        (member_id,) = cursor.fetchone()
        cursor.close()
        return member_id

    def get_row(self, table: str, address: str):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE address_evm = ?", (address,))
        tuple_answers = cursor.fetchone()
        cursor.close()
        return tuple_answers

    def get_child_code(self, tbl: str, atId: int) -> str:
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT member_id, referral_code FROM {tbl} WHERE member_id = ?", (atId,))
        (member_id, refrral_code) = cursor.fetchone()
        cursor.close()
        return refrral_code

    def keepcopy(self, file_path: str, r: Response):
        try:
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        except FileNotFoundError:
            with open(file_path, 'a+') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    def _update_resource_unsafe(self, address: str, res_file: dict):
        return self.update_member_table_unsafe(address, {
            "res": json.dumps(res_file)
        })

    def _update_resource_unsafe_from_id(self, user_id: str, res_file: dict):
        return self.update_col_unsafe_by_member_id(Galxi.DB_MEMBER, user_id, {
            "res": json.dumps(res_file)
        })

    # member session
    def insert_new(self, update_params: dict) -> bool:
        return self.insert_simple_row(Galxi.DB_MEMBER, update_params)

    def update_member_table_unsafe(self, address: str, update_param: dict) -> bool:
        return self.update_col_unsafe(Galxi.DB_MEMBER, address, update_param)

    def has_the_address(self, address: str) -> bool:
        return self.has_address(Galxi.DB_MEMBER, address)

    def has_the_id(self, twid: str) -> bool:
        return self.has_address(Galxi.DB_MEMBER, twid)

    def has_flag(self, key: str) -> bool:
        t = self.get_member_res(Galxi.DB_MEMBER, self.user_addr)
        if key in t:
            if isinstance(t[key], bool):
                return t[key]
            else:
                return False
        return False

    def _is_check_point_exist(self, key: str) -> bool:
        if self.has_address(Galxi.DB_MEMBER, self.user_addr) is False:
            return False
        dat_mem = self.get_next_action(Galxi.DB_MEMBER, self.user_addr)
        if key in dat_mem:
            return True
        return False

    def flag_up(self, key: str):
        da = self.get_member_res(Galxi.DB_MEMBER, self.user_addr)
        da.update({key: True})
        self._update_resource_unsafe(self.user_addr, da)

    def flag_down(self, key: str):
        da = self.get_member_res(Galxi.DB_MEMBER, self.user_addr)
        da.update({key: False})
        self._update_resource_unsafe(self.user_addr, da)

    def _check_point_update(self, key: str, how_long_seconds: int = 3600):
        self._check_point_update_res(Galxi.DB_MEMBER, self.user_addr, key, how_long_seconds)

    def _is_what_ready(self, key: str, df: bool = True) -> bool:
        return self._is_what_ready_res(Galxi.DB_MEMBER, self.user_addr, key, df)

    def _is_what_happen_delta(self, key: str, df: int = 0) -> int:
        return self._is_what_delta(Galxi.DB_MEMBER, self.user_addr, key, df)

    def _is_time_next_exists(self, key: str) -> bool:
        return self._is_time_exists(Galxi.DB_MEMBER, self.user_addr, key)

    def set_invalidate_token(self):
        if self.has_the_address(self.user_addr) is False:
            raise Exception("user is not found from the db")
        self._check_point_update("bearer_token_exp", 0)

    def register_new_evm_address(self, evm_address: str, file: dict) -> bool:
        ...

    def gen_user_id(self):
        return str(uuid.uuid1())

    def try_to_check_jwt_token(self, token):
        decoded_token = jwt.decode(jwt=token, options={"verify_signature": False}, verify=False)
        # Get the expiration timestamp from the decoded token
        expiration_timestamp = decoded_token.get('iat')
        if expiration_timestamp is None:
            return False, 0
        else:
            expiration_delta = expiration_timestamp - self.get_time_now()
            return True, expiration_delta

    def set_jwt_token(self, bearer: str):
        has_address = self.has_the_address(self.user_addr)
        jwtdecode = self.try_to_check_jwt_token(bearer)
        result, delta = jwtdecode
        if has_address:
            self.update_res_kv("bearer_token", bearer)
        else:
            self.register_new_evm_address(self.user_addr, {
                "bearer_token": bearer,
            })
        if result:
            self._check_point_update("bearer_token_exp", delta)
        else:
            self._check_point_update("bearer_token_exp", 3600)

        self.update_col_time()

    def check_bearer_token_expired(self) -> bool:
        return self._is_what_ready("bearer_token_exp")

    def get_access_token(self):
        if self.has_the_address(self.user_addr) is False:
            return ""
        if self.check_bearer_token_expired() is True:
            print("token expired")
            return ""
        d = self.get_member_res(Galxi.DB_MEMBER, self.user_addr)
        if "bearer_token" in d:
            f = str(d["bearer_token"]).replace("\n", "")
            return f
        else:
            return ""

    def get_key_res(self, key: str):
        da = self.get_member_res(Galxi.DB_MEMBER, self.user_addr)
        if key in da:
            return da[key]
        else:
            return ""

    def has_res_key(self, key: str):
        res = self.get_member_res(Galxi.DB_MEMBER, self.user_addr)
        return True if key in res else False

    def res_true(self, key: str) -> bool:
        res = self.get_member_res(Galxi.DB_MEMBER, self.user_addr)
        if key in res:
            res_bool = res[key]
            if isinstance(res_bool, bool):
                return res_bool
            else:
                return False
        else:
            return False

    def update_col_time(self):
        if self.has_update_time is False:
            return
        if self.has_the_address(self.user_addr) is False:
            return
        self.update_col_unsafe(Galxi.DB_MEMBER, self.user_addr, {"update_time": self.get_time_now()})

    def update_res_kv(self, key: str, val):
        da = self.get_member_res(Galxi.DB_MEMBER, self.user_addr)
        da.update({key: val})
        self._update_resource_unsafe(self.user_addr, da)
        self.update_col_time()

    def update_res_set(self, val: dict):
        da = self.get_member_res(Galxi.DB_MEMBER, self.user_addr)
        da.update(val)
        self._update_resource_unsafe(self.user_addr, da)
        self.update_col_time()

    # this is the part for the key value
    def kv_has_key(self, name_key: str):
        tbl = Galxi.DB_KV
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT key_name, value_content, update_time FROM {tbl} WHERE key_name = ?", (name_key,))
        db_result = cursor.fetchone()
        cursor.close()
        if db_result is None:
            return False
        else:
            return True

    def kv_get_value_pair(self, name_key: str):
        # returns the value and the timestamp
        tbl = Galxi.DB_KV
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT value_content, update_time FROM {tbl} WHERE key_name = ?", (name_key,))
        db_result = cursor.fetchone()
        cursor.close()
        return db_result

    def kv_set_pair(self, key: str, value, update_time: int = 0) -> bool:
        tbl = Galxi.DB_KV
        params = {
            "value_content": value,
            "update_time": self.get_time_now()
        }
        if update_time == 0:
            params.update({
                "update_time": self.get_time_now()
            })
        else:
            params.update({
                "update_time": update_time
            })
        if self.kv_has_key(key) is True:
            try:
                columns = obj_to_string(params)
                self.conn.execute(f"UPDATE {tbl} set {columns} WHERE key_name='{key}'")
            except Exception as E:
                db_logger.error('Data Update Error : ', E)
                return False
            self.conn.commit()
            return True
        else:
            params.update({
                "key_name": key
            })
            keys, vals = obj_to_tuple(params)
            # insert query
            try:
                query = (
                    f'INSERT INTO {tbl} ({keys}) VALUES ({vals})'
                )
                self.conn.execute(query, params)
                self.conn.commit()
            except (
                    sqlite3.OperationalError,
                    Exception
            ) as e:
                db_logger.error('Data Insert Error : ', e)
                return False
            return True


class GalaBox(MemberMgm):
    def __init__(self):
        self.has_update_time = True

        path_db = os.path.join(Galxi.CACHE_PATH, 'cache.db')
        schema = os.path.join(Galxi.CACHE_PATH, 'schema.json')
        self.cache_db_path = path_db
        new_db = False if os.path.isfile(path_db) else True
        super().__init__(
            db_name=path_db,
            db_config_file_path=schema,
            same_thread=False
        )

        if new_db:
            self.create_table()
        self.user_addr = ""

    def fix_connection_issue(self):
        self.conn = sqlite3.connect(self.cache_db_path, check_same_thread=False, timeout=30)

    def check_token_claim_ready(self) -> bool:
        return self._is_what_ready("token_claim")

    def check_point_token_claim(self, ms_second: int):
        self._check_point_update("token_claim", ms_second)

    def check_point_synced(self, cred_id: str):
        # + 9 hours after will be ready to do it again
        self._check_point_update(f"cred_{cred_id}", 32400)

    def is_task_just_done(self, cred_id: str, in_range: int = 3600):
        kv = self._is_what_happen_delta(f"cred_{cred_id}", 0)
        if kv == 0:
            return False
        kv = kv + 32400
        kv = int(math.fabs(float(kv)))
        if kv < in_range:
            return True
        else:
            return False

    def check_point_claim(self, cred_id: str):
        # + 30 sec after will be ready for this action
        self._check_point_update(f"cred_claim_{cred_id}", 30)

    def checked_email_mark_time(self):
        self._check_point_update("checked_email_code", 0)

    def checked_email_send_time(self):
        self._check_point_update("sent_email_expire", 3600)

    def reset_email_send_time(self):
        self._check_point_zero(Galxi.DB_MEMBER, self.user_addr, "sent_email_expire")

    def is_email_sent_expired(self):
        return self._is_what_ready("sent_email_expire")

    def is_email_sent(self):
        return self._check_point_recently(Galxi.DB_MEMBER, self.user_addr, "sent_email_expire")

    def is_email_sent_reset(self):
        return self._check_point_is_zero(Galxi.DB_MEMBER, self.user_addr, "sent_email_expire")

    def is_check_point_ready(self, cred_id: str):
        return self._is_what_ready(f"cred_{cred_id}")

    def check_claim_ready(self, cred_it: str):
        return self._is_what_ready(f"cred_claim_{cred_it}")

    def is_campaign_claimed_before(self, camp_id: str):
        return self._is_check_point_exist(camp_id)

    def check_point_campaign_done(self, camp_id: str):
        return self._check_point_update(f"campaign_claimed_{camp_id}", 0)

    def check_point_campaign(self, camp_id: str):
        return self._check_point_update(f"campaign_claimed_{camp_id}", 32400)

    def is_check_point_cp_ready(self, camp_id: str):
        return self._is_what_ready(f"campaign_claimed_{camp_id}", False)

    def register_new_evm_address(self, evm_address: str, file: dict) -> bool:
        p = {
            "member_id": self.gen_user_id(),
            "address_evm": self.user_addr,
            "parent_code": "",
            "referral_code": "",
            "next_action": "{}",
            "update_time": self.get_time_now(),
            "res": json.dumps(file)
        }
        return self.insert_new(p)

    def set_address(self, address_vibe: str):
        self.user_addr = address_vibe

    def is_twitter_account_bind(self) -> bool:
        da = self.get_member_res(Galxi.DB_MEMBER, self.user_addr)
        print(da)
        if "twitter_id" in da:
            twitter_id = da["twitter_id"]
            print(f"twitter account ID is found {twitter_id}")
            if twitter_id is None or twitter_id == "":
                return False
            else:
                return True
        return False

    def get_random_historic_parent_code(self) -> str:
        """
        the goal is to get the random child referral code from the existing table members
        :return:
        """
        try:
            count_members = self.total_count(Galxi.DB_MEMBER)
            if count_members > 10:
                random_number = random.randint(1, count_members)
            else:
                first_id = self.get_first_row(Galxi.DB_MEMBER)
                print(f"only use the first row ID", first_id)
                return self.get_child_code(Galxi.DB_MEMBER, first_id)
            print(f"check number {random_number}")
            if self.has_row(Galxi.DB_MEMBER, random_number) is True:
                return self.get_child_code(Galxi.DB_MEMBER, random_number)
            else:
                return self.get_random_historic_parent_code()

        except RecursionError:
            first_id = self.get_first_row(Galxi.DB_MEMBER)
            print(f"only use the first row ID", first_id)
            return self.get_child_code(Galxi.DB_MEMBER, first_id)

    def log_failed_verifications(self):
        if self.kv_has_key("verification_failure") is False:
            self.kv_set_pair("verification_failure", 1)
        else:
            (value, time_next) = self.kv_get_value_pair("verification_failure")
            self.kv_set_pair("verification_failure", int(value) + 1)


class RemoteDB(MemberMgm):
    # database merger
    def __init__(self, path_db: str):

        schema = os.path.join(Galxi.CACHE_PATH, 'schema.json')
        self.cache_db_path = path_db

        new_db = False if os.path.isfile(path_db) else True

        super().__init__(
            db_name=path_db,
            db_config_file_path=schema,
            same_thread=False
        )
        if new_db:
            print("db is not found. need to init DB")
        else:
            self.conn = sqlite3.connect(path_db, check_same_thread=False, timeout=30)
            print("DB is connected.", path_db)

    def merge_tbl1(self, target_db: MemberMgm):
        total_rows = target_db.total_count(Galxi.DB_MEMBER)
        rows_per_page = 1000
        table_f = f"SELECT * FROM {Galxi.DB_MEMBER} LIMIT ? OFFSET ?"
        for offset in range(0, total_rows, rows_per_page):
            cursor = self.conn.cursor()
            cursor.execute(table_f, (rows_per_page, offset))
            all_pool = cursor.fetchall()
            cursor.close()
            perc = float(offset) / float(total_rows)
            print("batch processing {:.2%}".format(perc))
            g = 0
            if perc < 0.75:
                continue

            for (member_id, address_evm, referral_code, parent_code, res, next_act, update_time) in all_pool:
                if target_db.has_the_address(address_evm) is False:
                    target_db.insert_new({
                        "member_id": member_id,
                        "address_evm": address_evm,
                        "parent_code": parent_code,
                        "referral_code": referral_code,
                        "next_action": next_act,
                        "update_time": update_time,
                        "res": res
                    })
                    print(f"new data record.{address_evm} {g}")
                else:
                    if update_time > target_db.get_mem_update_time(address_evm) is True:
                        target_db.update_member_table_unsafe(address_evm, {
                            "next_action": next_act,
                            "update_time": update_time,
                            "res": res
                        })
                        print("update record.", g, address_evm, end="\r")

                    else:
                        print("skip record.", g, address_evm, end="\r")

                g += 1


class MigrateUpgrade(MemberMgm):
    def __init__(self, file_cache: str):
        self.has_update_time = True
        path_db = os.path.join(Galxi.CACHE_PATH, file_cache)
        schema = os.path.join(Galxi.CACHE_PATH, 'schema.json')
        self.cache_db_path = path_db
        new_db = False if os.path.isfile(path_db) else True
        super().__init__(
            db_name=path_db,
            db_config_file_path=schema,
            same_thread=False
        )
        if new_db:
            self.create_table()
        self.user_addr = ""

    def merge_from_remote_db(self, target_db: MemberMgm, addresses_list: list[str]):
        total_rows = target_db.total_count(Galxi.DB_MEMBER)
        print(f"foreign db has rows:: {total_rows}")
        for address_galxe in addresses_list:
            if target_db.has_the_address(address_galxe) and self.has_the_address(address_galxe) is False:
                j = target_db.get_row(Galxi.DB_MEMBER, address_galxe)
                (id, addr, a, b, ne, res, upt) = j
                p = {
                    "member_id": id[:8],
                    "address_evm": addr,
                    "parent_code": a,
                    "referral_code": b,
                    "next_action": ne,
                    "update_time": upt,
                    "res": res
                }
                self.add_new_row(Galxi.DB_MEMBER, p)
                print(f"action on {address_galxe}", end="\r")
        self.statistic_job()

    def add_new_row(self, tbl: str, params: dict) -> bool:
        keys, vals = obj_to_tuple(params)
        try:
            query = (
                f'INSERT INTO {tbl} ({keys}) VALUES ({vals})'
            )
            self.conn.execute(query, params)
            self.conn.commit()
        except (
                sqlite3.OperationalError,
                Exception
        ) as e:
            db_logger.error('Data Insert Error : ', e)
            return False
        return True

    def fetch_all_from_member(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT address_evm, next_action, res FROM {Galxi.DB_MEMBER}")
        all_members = cursor.fetchall()
        cursor.close()
        return all_members

    def statistic_job_interval(self):
        if self.kv_has_key("stats_job") is False:
            self.kv_set_pair("stats_job", 1)
            return True
        else:
            d = self.kv_get_value_pair("stats_job")
            (value, time_next) = d
            if self.get_time_now() > int(time_next) + 3600 * 5:
                stats = int(value) + 1
                self.kv_set_pair("stats_job", stats)
                return True
            else:
                return False

    def statistic_job(self):
        if self.statistic_job_interval() is False:
            return

        total_dp = self.total_count(Galxi.DB_MEMBER)
        self.kv_set_pair("total_member", int(total_dp))
        all_members = self.fetch_all_from_member()
        # this is the example for the statistic job

        f1 = 0
        f2 = 0
        f3 = 0
        f4 = 0

        for (address, next_act, res) in all_members:
            ...

        self.kv_set_pair("...", f1)
        self.kv_set_pair("...", f2)
        self.kv_set_pair("...", f3)
        self.kv_set_pair("...", f4)
