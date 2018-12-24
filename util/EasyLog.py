#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : EasyLog.py
# @Author: MoonKuma
# @Date  : 2018/11/22
# @Desc  : write log message into files (/log/log_${date}.log)

import logging
import time
import log.log_local as log_local
import sys


class EasyLog(object):
    def __init__(self, class_name='General', log_type='test', to_console = True):
        self.logger = logging.getLogger(class_name)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s')
        log_type_dict = {'statistic': log_local.statistic_log_patten, 'socket': log_local.socket_log_patten, 'test': log_local.test_log_patten}
        log_file = log_type_dict.setdefault(log_type, log_local.test_log_patten) + time.strftime("_%Y-%m-%d.log", time.localtime())
        msg = 'Log file for ' + class_name + ' maintained in: ' + log_file
        print(msg)
        file_handler = logging.FileHandler(log_file, 'a+')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        if to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


# test main
if __name__ == '__main__':
    log_obj1 = EasyLog(EasyLog.__name__)
    log_obj2 = EasyLog('SomeOtherName')
    line_num = 0
    for i in range(0, 10):
        line_num += 1
        msg = 'some info msg from log_obj1 for ' + str(line_num) + ' time(s)'
        log_obj1.info(msg)
        log_obj2.info(msg)



