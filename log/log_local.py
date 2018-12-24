#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : log_local.py
# @Author: MoonKuma
# @Date  : 2018/11/22
# @Desc  : show log location for different log type

import os

current_path = os.path.realpath(os.path.abspath(os.path.split(__file__)[0]))
statistic_log_patten = os.path.join(current_path,'statistic_log')
test_log_patten = os.path.join(current_path,'test_log')
socket_log_patten = os.path.join(current_path,'socket_log')
