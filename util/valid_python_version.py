#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : valid_python_version.py
# @Author: MoonKuma
# @Date  : 2018/12/12
# @Desc  : test if python version is correct for certain method


import sys
# import traceback

def valid_python_major(version):
    msg = 'You are using: Python' + str(sys.version_info[0])
    print(msg)
    if str(version) != str(sys.version_info[0]):
        msg = '[ERROR]Invalid python version: Python' +  str(version) + ' is expected, while Python' + str(sys.version_info[0]) + ' is used.'
        print(msg)
        raise RuntimeError

# test
if __name__ == '__main__':
    valid_python_major(3)
