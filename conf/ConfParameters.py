#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ConfParameters.py
# @Author: MoonKuma
# @Date  : 2018/8/31
# @Desc  : Environmental parameters


class ConfParameters:
    def __init__(self):
        self.mysql_conf = dict()
        self.mysql_conf_bd = dict()
        self.mysql_conf_bd_test = dict()
        self.socket_conf = dict()
        self.socket_conf_xf = dict()
        self.log_conf = dict()
        self.save_path = ''
        self.conf_path = ''
        self.load()

    def load(self):
        # mysql_conf

        # mysql_conf_bd

        # mysql_conf_bd_test

        # socket_conf
        self.socket_conf['ip'] = '196.169.1.1'
        self.socket_conf['port'] = 10000
        # socket_conf_xf
        self.socket_conf_xf['ip'] = '196.169.1.1'
        self.socket_conf_xf['port'] = 10000
        # log_conf

        # save_path
        self.save_path = '/data/'
        self.conf_path = '/data/'

    def show_component(self):
        co_list = list(self.__init__.func_code.co_names)
        co_list.remove('dict')
        co_list.remove('load')
        return co_list

    def show_details(self, *component_name):
        obj = ConfParameters()
        if len(component_name) > 0:
            print(component_name[0], ':', getattr(obj, component_name[0], 'not found'))
            return
        co_list = self.show_component()
        for component in co_list:
            print(component, ':', getattr(obj, component, 'not found'))


