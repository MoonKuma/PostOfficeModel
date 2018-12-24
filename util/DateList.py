#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : DateList.py
# @Author: MoonKuma
# @Date  : 2018/8/30
# @Desc  : Generate a date list with certain format

import datetime


class DateList:
    def __init__(self):
        self.format = '%Y-%m-%d'
        self.month_format = '%Y-%m'

    def set_format(self, new_format):
        self.format = new_format

    def set_month_format(self, new_month_format):
        self.month_format = new_month_format

    def get_format(self):
        return self.format

    def get_date_list(self, stat_date, end_date):
        date_list = list()
        d1 = datetime.datetime.strptime(stat_date, self.format)
        d2 = datetime.datetime.strptime(end_date, self.format)
        day_diff = (d2 - d1).days
        while day_diff >= 0:
            date_list.append(d1.strftime(self.format))
            d1 = d1 + datetime.timedelta(days=1)
            day_diff = (d2 - d1).days
        return date_list

    def get_today(self):
        return (datetime.datetime.now()).strftime(self.format)

    def add_date(self, date_in, add_num):
        d1 = datetime.datetime.strptime(date_in, self.format)
        d2 = d1 + datetime.timedelta(days=int(add_num))
        return d2.strftime(self.format)

    def get_last_week(self):
        date0 = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime(self.format)
        date1 = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(self.format)
        return [date0, date1]

    def get_next_month(self, month_str):
        month = datetime.datetime.strptime(month_str, self.month_format)
        new_month = (month.month + 1)%12
        new_year = month.year
        if month.month == 12:
            new_year +=1
        next_month = datetime.datetime(new_year, new_month, 1)
        return next_month.strftime(self.month_format)




# test main
if __name__ == '__main__':
    print(DateList().get_today())
    print(DateList().get_last_week())
    print(DateList().get_next_month('2018-12'))





