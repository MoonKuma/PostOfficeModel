#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : UserInfoCheck.py
# @Author: MoonKuma
# @Date  : 2018/9/5
# @Desc  : Check user's information like register date and total payment

import time


class UserInfoCheck:
    def __init__(self, cursor):
        self.cursor = cursor
        return

    def get_reg_info(self, stat_base, user_active_openid, uid):
        # check the register date for certain uid (use min date as register date for safety reason)
        result = dict()
        result['channel'] = 'not_found'
        result['zoneid'] = 'not_found'
        result['min_date'] = 'not_found'
        result['max_date'] = 'not_found'
        sql_str = 'select min(date),max(date),max(zoneid),max(channel) from ' +stat_base+ '.'+user_active_openid+' where uid=\'' + uid + '\' group by uid'
        self.cursor.execute(sql_str)
        all_data = self.cursor.fetchall()
        if all_data:
            for rec in all_data:
                result['min_date'] = str(rec[0])
                result['max_date'] = str(rec[1])
                result['zoneid'] = str(rec[2])
                result['channel'] = str(rec[3])
                break
        return result

    def get_total_payment(self, stat_pay, uid):
        # check the total payment of certain uid
        payment = 0
        sql_str = 'select sum(money/100) from ' + stat_pay + '.pay_syn_day where uid=\'' + uid + '\''
        self.cursor.execute(sql_str)
        all_data = self.cursor.fetchall()
        if all_data:
            for rec in all_data:
                try:
                    payment = float(rec[0])
                except:
                    payment = 0
        return payment

    def get_user_name(self, t_player_db, uid):
        # there will be 0.1s sleep when checking this term, in case the select operation block the login process
        user_name = 'NotFound'
        time.sleep(0.1)
        sql_str = 'select from_base64(name) from ' + t_player_db + '.t_player where uid = \'' + uid + '\''
        self.cursor.execute(sql_str)
        all_data = self.cursor.fetchall()
        if all_data:
            for rec in all_data:
                user_name = rec[0]
        return user_name




