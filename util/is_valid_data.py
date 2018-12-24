#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : is_valid_data.py
# @Author: MoonKuma
# @Date  : 2018/10/26
# @Desc  : testify whether input/output dicts are legal


def is_legal_input(input_dict):
    key_list_dict = {'date_list': list(), 'zone_list': list(), 'channel_list': list(), 'cursor': None}
    for key in key_list_dict.keys():
        validity = __test_data_type(input_dict, key, key_list_dict[key])
        if validity == 999:
            continue
        elif validity == 0:
            msg = '[InputError]Key:' + str(key) + ' does not exist in output dict'
            raise RuntimeError(msg)
        elif validity == 1:
            msg = '[InputError]Key:' + str(key) + ' type is ' + str(type(input_dict[key])) + ', while required type is:' + str(type(key_list_dict[key]))
            raise RuntimeError(msg)


def is_legal_output(res_dict):
    key_list_dict = {'data_dict': dict(), 'X_list': list(), 'Y_list': list(), 'head_name': str(), 'default_value': None}
    for key in key_list_dict.keys():
        validity = __test_data_type(res_dict, key, key_list_dict[key])
        if validity == 999:
            continue
        elif validity == 0:
            msg = '[OutputError]Key:' + str(key) + ' does not exist in output dict'
            raise RuntimeError(msg)
        elif validity == 1:
            msg = '[OutputError]Key:' + str(key) + ' type is ' + str(type(res_dict[key])) + ', while required type is:' + str(type(key_list_dict[key]))
            raise RuntimeError(msg)
    

# native method
def __test_data_type(data_dict, data_key , test_type):
    if data_key not in data_dict.keys():
        return 0
    data_value = data_dict[data_key]
    if type(test_type) == type(None):
        return 999
    if type(data_value) == type(test_type):
        return 999
    else:
        return 1