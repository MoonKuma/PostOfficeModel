#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : LogQuery.py
# @Author: MoonKuma
# @Date  : 2018/9/11
# @Desc  : Query log based on current environment

import conf.ConfParameters as ConfParameters
import DateList
import os
# from abc import ABCMeta, abstractmethod


class LogQuery(object):

    def __init__(self, start_date, end_date):
        self.conf = ConfParameters.ConfParameters()
        self.log_path = self.conf.log_conf['game_log_path_current']
        self.stat_path = self.conf.log_conf['stat_log_path']
        self.date_list = DateList.DateList().get_date_list(start_date,end_date)

    def log_file_str(self):
        date_list = self.date_list
        file_list = list()
        file_str = ''
        for date in date_list:
            file_name = self.log_path.replace('$dateString$', date)
            file_list.append(file_name)
        for file_name in file_list:
            file_str = file_str + ' ' + file_name
        return file_str

    def event_file_str(self):
        date_list = self.date_list
        file_list = list()
        file_str = ''
        for date in date_list:
            if date == self.date_obj.get_today():
                file_name = self.stat_path + 'event.log'
            else:
                file_name = self.stat_path + 'event.log.' + date
            file_list.append(file_name)
        for file_name in file_list:
            file_str = file_str + ' ' + file_name
        return file_str

    def cmd_compute(self, cmd_str):
        print(cmd_str)
        val = os.popen(cmd_str).readlines()
        return val

    def get_file_type(self, path):
        filename, file_type = os.path.splitext(path)
        return file_type

    def cmd_compute_write_txt(self, cmd_str, short_file_name):
        file_name = self.conf.save_path + short_file_name
        if self.get_file_type(file_name) != '.txt':
            msg = 'This method is not applicable for non-txt files. Return None'
            print(msg)
            return None
        result = self.cmd_compute(cmd_str)
        with open(file_name, 'w') as f:
            for line in result:
                line = line.strip()
                line = line + '\n'
                f.write(line)
            return 1
        msg = ''

    def analyse_log(self, log_data): pass









