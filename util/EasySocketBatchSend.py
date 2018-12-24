#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : EasySocketBatchSend.py
# @Author: MoonKuma
# @Date  : 2018/12/11
# @Desc  : Using threadpool to control the num of thread active
# Caution : sid for each cmd is added inside method, input cmd_list should contain no sid or \n in the end

from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from util import EasyLog
from util import EasySocketBatch

class EasySocketBatchSend(object):

    def __init__(self, ip, port, worker=50):
        """
        Initializes a new EasySocketBatchSend instance.
        Args:
        	ip: socket ip
        	port: socket port
        	worker: number of threads in threadpool, default 50

        """
        self.ip = str(ip)
        self.port = int(port)
        self.easy_log_conceal = EasyLog.EasyLog(self.__class__.__name__, 'socket', to_console=False)
        self.easy_log_show = EasyLog.EasyLog(self.__class__.__name__, 'socket', to_console=True)
        # local parameter
        self.easy_sock = EasySocketBatch.NetConnection(self.ip, self.port)
        self.worker = worker
        self.executor = ThreadPoolExecutor(max_workers=self.worker)
        # result

    def run_cmd_list(self, cmd_list):
        """
        Run requests list until all results returned (received or time out)

        Args:
        	cmd_list: list of request, according to current protocol, the full request should be like XXXX, sid\n, yet here only the XXXX part is legal and required, for system will add ,sid\n part automatically.

        Returns:
            result_list : list of result for each request, each result are packed up like [full request, result json], thus the the result list returned looks like [[request1,json1],[requset2,json2],...]

        Raises:
            RuntimeError: If the length of receiving list fails to match the requesting list

        """
        msg = 'Start committing cmd to socket local' + str(self.ip) + ":" + str(self.port) + " with " + str(self.worker) + "workers."
        self.easy_log_show.info(msg)
        # future_list = list()
        # for cmd in cmd_list:
        #     cmd = cmd.strip()
        #     # self.easy_log_conceal.info(cmd)
        #     future = self.executor.submit(self.__thread_func,cmd,)
        #     future_list.append(future)
        # future_results = list()
        # futures.wait(future_list)
        # for future in future_list:
        #     future_results.append(future.result())
        future_results = list(self.executor.map(self.__thread_func, cmd_list, timeout=10)) # map works in the same way
        if len(cmd_list) != len(future_results):
            msg = str(len(cmd_list)) + ' cmd message is sent, while ' + str(len(future_results)) + ' was return'
            self.easy_log_show.error(msg)
            raise RuntimeError
        msg = 'Run success! ' + str(len(cmd_list)) + ' cmd message is sent,' + str(len(future_results)) + ' was returned'
        self.easy_log_show.info(msg)
        return future_results

    def quit_receiving(self):
        """
        Stop receiving to end the whole progress of current socket work.
        This func should be called when no more requests are going to be sent to through current socket connection, or the main progress won't exit
        Once quit_receiving is called, no more message will be sent successfully.

        """
        self.easy_sock.quit_receive()

    def __thread_func(self, cmd):
        return self.easy_sock.send_cmd(cmd)

