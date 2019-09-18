#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step04_download_hkex_statistics_data
# @Date: 2019/9/17
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.step04_download_hkex_statistics_data
"""

import os
import re
import time
import json
import requests
import datetime

import numpy as np
from tqdm import tqdm
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const


def download_stock_market_statistics(year, month, day):
    base_url = 'https://www.hkex.com.hk/eng/csm/ws/Highlightsearch.asmx/GetData'
    req = requests.get(base_url + '?LangCode=en&TDD={day}&TMM={month}&TYYYY={year}&_={requests_time}'.format(
        day=day, month=month, year=year, requests_time=int(time.time() * 1e4)))

    request_data = json.loads(req.text)['data']

    result_dfs = [dict() for _ in [1, 2, 3]]

    for i in [1, 2, 3]:
        d, m, y = re.findall(r'\d+', request_data[0]['td'][i][0])
        if int(d) != day or int(m) != month or int(y) != year:
            continue

        sub_cat1, sub_cat2 = request_data[1]['td'][i]

        for j in range(2, 11):
            column_name = request_data[j]['td'][0][0].replace('<br>', ' ')
            sub_info1, sub_info2 = request_data[j]['td'][i]
            result_dfs[i - 1]['{} ({})'.format(column_name, sub_cat1)] = sub_info1
            result_dfs[i - 1]['{} ({})'.format(column_name, sub_cat2)] = sub_info2

        result_dfs[i - 1][request_data[11]['td'][0][0].replace('<br>', ' ')] = request_data[11]['td'][i][0]

    return result_dfs


if __name__ == '__main__':
    start_date = datetime.datetime(2019, 8, 1)
    end_date = datetime.datetime(2019, 9, 15)

    hk_data_list = []
    sh_data_list = []
    sz_data_list = []

    for d in tqdm(pd.date_range(start=start_date, end=end_date, freq='D')):
        hk_data, sh_data, sz_data = download_stock_market_statistics(d.year, d.month, d.day)

        if hk_data:
            hk_data[const.DATE] = d
            hk_data_list.append(hk_data)

        if sh_data:
            sh_data[const.DATE] = d
            sh_data_list.append(sh_data)

        if sz_data:
            sz_data[const.DATE] = d
            sz_data_list.append(sz_data)

    sz_data_df: DataFrame = DataFrame(sz_data_list).replace('n.a.', np.nan)
    sh_data_df: DataFrame = DataFrame(sh_data_list).replace('n.a.', np.nan)
    hk_data_df: DataFrame = DataFrame(hk_data_list).replace('n.a.', np.nan)

    sz_data_df.to_pickle(os.path.join(const.TEMP_PATH, '20190917_sz_stock_market_stat.pkl'))
    sh_data_df.to_pickle(os.path.join(const.TEMP_PATH, '20190917_sh_stock_market_stat.pkl'))
    hk_data_df.to_pickle(os.path.join(const.TEMP_PATH, '20190917_hk_stock_market_stat.pkl'))
