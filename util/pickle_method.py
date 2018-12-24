#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : pickle.py
# @Author: MoonKuma
# @Date  : 2018/12/7
# @Desc  :
import copy_reg
import types
import multiprocessing


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)


copy_reg.pickle(types.MethodType, _pickle_method)


class Controler(object):
    def __init__(self):
        nProcess = 10
        pages = 10
        self.__result = []
        self.manageWork(nProcess, pages)

    def BarcodeSearcher(self, x):
        return x*x

    def resultCollector(self, result):
        self.__result.append(result)

    def manageWork(self, nProcess, pages):
        pool = multiprocessing.Pool(processes=nProcess)
        for pag in range(pages):
            pool.apply_async(self.BarcodeSearcher, args=(pag,),
                             callback=self.resultCollector)
        pool.close()
        pool.join()

        print(self.__result)

if __name__ == '__main__':
    Controler()