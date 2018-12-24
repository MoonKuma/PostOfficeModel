#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : WriteStandardForm.py
# @Author: MoonKuma
# @Date  : 2018/10/26
# @Desc  : write standard result into sheet

from util.is_valid_data import is_legal_output
import util.EasyXls as EasyXls


def write_standard_form(res_dict,sheet,line_num,style):
    is_legal_output(res_dict)
    data_dict = res_dict['data_dict']
    X_list = res_dict['X_list']
    Y_list = res_dict['Y_list']
    head_name = res_dict['head_name']
    default_value = res_dict['default_value']
    X_trans = res_dict.setdefault('X_trans', dict())
    Y_trans = res_dict.setdefault('Y_trans', dict())

    easy_xls = EasyXls.EasyXls()
    head_list = list()
    head_list.append(head_name)
    for X in X_list:
        head_list.append(X_trans.setdefault(X, X))
    easy_xls.insert_xls_style(head_list, sheet, line_num, style)
    for Y in Y_list:
        data_list = list()
        data_list.append(Y_trans.setdefault(Y, Y))
        for X in X_list:
            data_list.append(data_dict.setdefault(Y, dict()).setdefault(X, default_value))
        easy_xls.insert_xls_style(data_list, sheet, line_num, style)
