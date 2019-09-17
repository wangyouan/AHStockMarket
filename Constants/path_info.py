#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: path_info
# @Date: 2019/9/17
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

PROJECT_NAME = 'AHStockMarket'


class PathInfo(object):
    ROOT_PATH = '/home/zigan/Documents/wangyouan/study/AHStockMarket'

    DATA_PATH = os.path.join(ROOT_PATH, 'data')
    TEMP_PATH = os.path.join(ROOT_PATH, 'temp')
    RESULT_PATH = os.path.join(ROOT_PATH, 'result')

    DATABASE_PATH = '/home/zigan/Documents/wangyouan/database'
