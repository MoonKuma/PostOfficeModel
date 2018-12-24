#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : SocketBatchedPlayerInfo.py
# @Author: MoonKuma
# @Date  : 2018/11/28
# @Desc  : Test EasySocketCmd.send_patch_cmd

# valid python
from util.valid_python_version import valid_python_major
valid_python_major(3)
import conf.ConfParameters as ConfParameters
import util.EasySocketBatch as EasySocketBatch
import util.EasySocketCmd as EasySocketCmd
import util.EasySocketBatchSend as EasySocketBatchSend
import util.EasyLog as EasyLog
import sys
import time
import threading
import random
import socket
import traceback


# override a new thread object to get return
class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        # self.result = self.func(*self.args) # this is incorrect, if the running part is executed here than there is no need for threading
        self.result = None

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


# test with player info
class SocketBatchedPlayerInfo(object):
    def __init__(self):

        # initial socket
        self.sk_conf = ConfParameters.ConfParameters().socket_conf_xf
        ip_port = (self.sk_conf['ip'], self.sk_conf['port'])
        # log module
        self.easy_log = EasyLog.EasyLog(self.__class__.__name__, 'socket')
        # local parameter
        self.easy_sock = EasySocketBatch.NetConnection(ip_port[0], ip_port[1])
        # result
        self.result_dict = dict()

    @staticmethod
    def get_cmd_list(uid_list):
        # playerinfo,u72339077604641602,48742804
        cmd_list = list()
        for uid in uid_list:
            cmd = 'playerinfo,u' + str(uid)
            # self.easy_log.info(cmd)
            cmd_list.append(cmd)
        return cmd_list

    def thread_func(self, cmd):
        return self.easy_sock.send_cmd(cmd)

    def thread_func_test(self, cmd):
        time.sleep(1)
        return dict()

    def quit_receive(self):
        self.easy_sock.quit_receive()

    @staticmethod
    def dissect_result(result_dict):
        count = 0
        valid = 0
        match = 0
        for key in result_dict.keys():
            count += 1
            if result_dict[key] is not None:
                valid += 1
                key_s = key.strip()
                key_list = key_s.split(',')
                if 'uid' in result_dict[key].keys() and len(key_list)>2 and key_list[1][key_list[1].find('u')+1:] == (result_dict[key]['uid']):
                    match += 1
        msg = '[Result report]Count:' + str(count) + ', valid:' + str(valid) + ', matched:' + str(match)
        print(msg)
        # print(result_dict)


    @staticmethod
    def execute_func(uid_list):
        result_dict = dict()
        self = SocketBatchedPlayerInfo()
        # log_factory = EasyLog.EasyLog(self.__class__.__name__, 'socket')
        cmd_list = self.get_cmd_list(uid_list)
        time_start = time.time()
        print('[Threading]start at ', time.ctime())
        thread_list = list()
        for index in range(0,len(cmd_list)):
            # random_int = random.randint(1, 10)
            # t = MyThread(func= self.test_func, args=(cmd_list[index],random_int,), name=self.test_func.__name__)
            t = MyThread(func=self.thread_func, args=(cmd_list[index],), name=self.thread_func.__name__)
            thread_list.append(t)
        for index in range(0, len(cmd_list)):
            thread_list[index].start()
        print('[Threading]after all start at ', time.ctime())
        for index in range(0, len(cmd_list)):
            thread_list[index].join()
        for index in range(0, len(cmd_list)):
            [cmd, result] = thread_list[index].get_result()
            result_dict[cmd] = result
        print('[Threading]finish at ', time.ctime(), ',with len(result_dict.keys()):', len(result_dict.keys()), ',time cost:', str(time.time()-time_start))
        # time.sleep(5)
        # print(result_dict)
        self.quit_receive()
        self.dissect_result(result_dict)

    @staticmethod
    def run_without_thread(uid_list):
        cmd_list = SocketBatchedPlayerInfo.get_cmd_list(uid_list)
        easy_sock = EasySocketCmd.EasySocketCmd()
        result_dict = dict()
        sk_conf = ConfParameters.ConfParameters().socket_conf_xf
        ip_port = (sk_conf['ip'], sk_conf['port'])
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect(ip_port)
        sk.settimeout(2)
        sid = 1
        time_start = time.time()
        # log_factory = EasyLog.EasyLog(self.__class__.__name__, 'socket')
        print('[Original]start at ', time.ctime())
        for cmd in cmd_list:
            cmd_send = cmd + ',' + str(sid) + '\n'
            sid += 1
            try:
                result_dict[cmd_send] = easy_sock.send_cmd_message(cmd_send, sk)
            except Exception:
                print(traceback.format_exc())
        print('[Original]finish at ', time.ctime(), ',with len(result_dict.keys()):', len(result_dict.keys()), ',time cost:', str(time.time()-time_start))
        # time.sleep(5)
        # print(result_dict)
        SocketBatchedPlayerInfo.dissect_result(result_dict)

    @staticmethod
    def run_in_package(uid_list):
        cmd_list = SocketBatchedPlayerInfo.get_cmd_list(uid_list)
        sk_conf = ConfParameters.ConfParameters().socket_conf_xf
        sk_obj = EasySocketBatchSend.EasySocketBatchSend(sk_conf['ip'], sk_conf['port'])
        time_start = time.time()
        print('[Threading Batch]start at ', time.ctime())
        result_list = sk_obj.run_cmd_list(cmd_list)
        print('[Threading]finish at ', time.ctime(), ',with len(result_dict.keys()):', len(result_list),
              ',time cost:', str(time.time() - time_start))
        result_dict = dict()
        for result in result_list:
            result_dict[result[0]] = result[1]
        sk_obj.quit_receiving()
        # print(result_dict)
        SocketBatchedPlayerInfo.dissect_result(result_dict)

    def test_func(self, cmd, time_wait):
        time.sleep(time_wait)
        print('Sleeping over:' + str(time_wait) + ',cmd=' + cmd)



# test main
if __name__ == '__main__':
    print('*************')
    print('*           *')
    print('*   START   *')
    print('*           *')
    print('*************')
    # get uid list
    file_name = sys.argv[1]
    uid_list = list()
    file_open = open(file_name, 'r')
    for line in file_open.readlines():
        line = line.strip()
        if line not in uid_list:
            uid_list.append(line)
    # msg = 'Length uid_list = ' + str(len(uid_list)) + ' ,continue?(y/n)'
    # receive = raw_input(msg)
    # if receive.lower() == 'y':
    #
    # uid_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    SocketBatchedPlayerInfo.execute_func(uid_list)
    SocketBatchedPlayerInfo.run_without_thread(uid_list)
    SocketBatchedPlayerInfo.run_in_package(uid_list)
    # cmd_list = [1,2,3,4,5,6,7,8,9]
    # result_dict = dict()
    # print('start at ', time.ctime())
    # thread_list = list()
    # for index in range(0, len(cmd_list)):
    #     t = MyThread(test_func, (cmd_list[index],), test_func.__name__)
    #     thread_list.append(t)
    # for index in range(0, len(cmd_list)):
    #     thread_list[index].start()
    # for index in range(0, len(cmd_list)):
    #     thread_list[index].join()
    # for index in range(0, len(cmd_list)):
    #     result_dict[cmd_list[index]] = thread_list[index].get_result()
    # print('finish at ', time.ctime(), ',with len(result_dict.keys()):', len(result_dict.keys()))
    # print result_dict
