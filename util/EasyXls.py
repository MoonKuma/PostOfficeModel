#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : EasyXls.py
# @Author: MoonKuma
# @Date  : 2018/8/31
# @Desc  : including loading xls by line, and checking possible chinese characters


import re
import sys
import xlwt


class EasyXls:
    def __init__(self):
        self.zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        # default_encoding = 'utf-8'
        # if sys.getdefaultencoding() != default_encoding:
        #     reload(sys)
        #     sys.setdefaultencoding(default_encoding)
        self.borders = xlwt.Borders()
        self.borders.left = 1
        self.borders.right = 1
        self.borders.top = 1
        self.borders.bottom = 1
        self.borders.bottom_colour = 0x3A

    def contain_zh(self, word):
        # match = self.zh_pattern.search(unicode(word))
        match = self.zh_pattern.search(word)
        return match

    def insert_xls(self, data_list, sheet, line_num):
        # 按行写入xls
        line = line_num[0]
        for col in range(0, len(data_list)):
            if self.contain_zh(data_list[col]):
                sheet.write(line, col, data_list[col])
            else:
                sheet.write(line, col, data_list[col])
        line_num[0] = line + 1

    def insert_xls_style(self, data_list, sheet, line_num, style):
        # 按行写入xls，增加格式
        line = line_num[0]
        for col in range(0, len(data_list)):
            if self.contain_zh(data_list[col]):
                sheet.write(line, col, data_list[col], style)
            else:
                sheet.write(line, col, data_list[col], style)
        line_num[0] = line + 1

    def new_sheet(self, sheet_name, wbk):
        # 新建一个sheet表格
        return wbk.add_sheet(sheet_name, cell_overwrite_ok=True)
