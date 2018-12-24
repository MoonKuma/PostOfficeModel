#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : EasySocketCmd.py
# @Author: MoonKuma
# @Date  : 2018/9/13
# @Desc  : Send Cmd to game and receive data

import json
# import threadpool
import time
import util.EasyLog as EasyLog
class EasySocketCmd:

    def __init__(self):
        self.receive_list = list()
        self.log = EasyLog.EasyLog(self.__class__.__name__, 'socket', False)
        return

    def send_cmd_message(self, cmd, sk):
        self.log.info(cmd)
        sk.sendall(cmd.encode())
        # print(cmd)
        json_data = ''
        first_receive = 1
        total_length = 0
        while True:
            data = sk.recv(512).decode()
            # print(data)
            if first_receive == 1:
                string_length = data[0:data.find('{')]
                total_length = int(string_length, 16)
                first_receive = 0
                data = data[data.find('{'):]
            json_data = json_data + data
            if len(json_data) >= total_length:
                break
        result = json.loads(json_data)  # dict
        # self.receive_list.append(result) # sk.receive should be initialized as independent listener
        # time.sleep(1) #use for testify
        return result

    # def send_patch_cmd(self, cmd_list, sk):
    #     # caution: python is not very much fast in threading as in other language, but on the contrary, it's always safe in stucutres like list,dict,tuple (See GIL)
    #     self.receive_list = list()
    #     task_pool = threadpool.ThreadPool(50)
    #     func_var = list()
    #     for cmd in cmd_list:
    #         func_var.append(([cmd, sk], None))
    #     requests = threadpool.makeRequests(self.send_cmd_message, func_var)
    #     map(task_pool.putRequest, requests)
    #     task_pool.wait()
    #     return self.receive_list


#     def test_thread_pool(self, arg_list, arg_value):
#         self.receive_list = list()
#         task_pool = threadpool.ThreadPool(50)
#         func_var = list()
#         for cmd in arg_list:
#             func_var.append(([cmd,arg_value],None))
#         requests = threadpool.makeRequests(self.test_func, func_var)
#         map(task_pool.putRequest, requests)
#         task_pool.wait()
#         return self.receive_list
#
#     def test_func(self, cmd, arg_value):
#         msg = ',cmd:' + str(cmd) + 'arg_value:' + str(arg_value)
#         print(msg)
#         self.receive_list.append(cmd+1000)
#
#     @staticmethod
#     def execute_test():
#         arg_list = range(0,100)
#         print(EasySocketCmd().test_thread_pool(arg_list, '*test value*'))
#
#
# # test main
# if __name__ == '__main__':
#     EasySocketCmd.execute_test()
