#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ReadTable.py
# @Author: MoonKuma
# @Date  : 2018/9/7
# @Desc  : Read table into dict(), also could be used to check if file exits

import os
import collections


class ReadTable:

    def __init__(self, file_name):
        self.file_name = file_name
        self.index = [1, 1]  # use first line and row and index

    def reset_file_name(self, file_name):
        self.file_name = file_name

    def __reset_index(self, new_index):
        self.index = [int(new_index[0]), int(new_index[1])]

    def is_legal_file(self):
        return os.path.exists(self.file_name)

    def read_table_file(self, *index):  # plaint dict like {Y1|X1: value1, Y1|X2: value2, ...}
        result = collections.OrderedDict()
        if len(index) == 2:
            self.__reset_index(index)
        if self.is_legal_file():
            file_open = open(self.file_name)
            tmp_list = list()
            for line in file_open.readlines():
                line = line.strip()
                array = line.split('\t')
                tmp_list.append(array)
            for i in range(0, len(tmp_list)):
                for j in range(0, len(tmp_list[0])):
                    if i+1 == self.index[0] or j + 1 == self.index[1]:
                        continue
                    else:
                        key_y = tmp_list[i][self.index[1]-1]
                        key_x = tmp_list[self.index[0]-1][j]
                        key_combine = key_y + '|' + key_x
                        if key_combine not in result.keys():
                            result[key_combine] = tmp_list[i][j]
                        else:
                            result[key_combine] = tmp_list[i][j]
                            print ('multiple key :', key_combine)
            return result
        else:
            error_str = 'No such file named:', self.file_name
            raise RuntimeError(error_str)

    def read_table_file_coupled(self, *index):  # coupled dict like {Y1:{X1:value1, X2:value2...}, Y2:...}
        result = collections.OrderedDict()
        if len(index) == 2:
            self.__reset_index(index)
        if self.is_legal_file():
            file_open = open(self.file_name)
            tmp_list = list()
            for line in file_open.readlines():
                line = line.strip()
                array = line.split('\t')
                tmp_list.append(array)
            for i in range(0, len(tmp_list)):
                for j in range(0, len(tmp_list[0])):
                    if i+1 == self.index[0] or j + 1 == self.index[1]:
                        continue
                    else:
                        key_y = tmp_list[i][self.index[1]-1]
                        key_x = tmp_list[self.index[0]-1][j]
                        value = tmp_list[i][j]
                        if key_y not in result.keys():
                            result[key_y] = dict()
                        if key_x in result[key_y].keys():
                            print ('multiple key :', key_y, '|', key_x)
                        result[key_y][key_x] = value
            return result
        else:
            error_str = 'No such file named:', self.file_name
            raise RuntimeError(error_str)
