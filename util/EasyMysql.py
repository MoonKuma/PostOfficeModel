#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : EasyMysql.py
# @Author: MoonKuma
# @Date  : 2018/9/12
# @Desc  : Some useful tools in in mysql computing


class EasyMysql:

    def __init__(self):
        self.cycle = 100

    def set_cycle(self, cycle):
        self.cycle = cycle

    def sql_value_str(self, value_list):
        value_str = '\'' + str(value_list[0]) + '\''
        if len(value_list) > 1:
            for value_index in range(1, len(value_list)):
                value_str = value_str + ',\'' + str(value_list[value_index]) + '\''
        return value_str

    def batch_commit(self, sql_str_list, cursor, db):
        msg =  '[Batch Commit] Start committing to db with ' + str(len(sql_str_list)) + ' commend lines'
        print(msg)
        cycle = self.cycle
        count = 0
        list_len = len(sql_str_list)
        for line in sql_str_list:
            count += 1
            cursor.execute(line)
            if count % cycle == 0 or count >= list_len:
                db.commit()
        db.commit()