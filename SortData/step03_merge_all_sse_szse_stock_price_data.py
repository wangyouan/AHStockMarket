#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step03_merge_all_sse_szse_stock_price_data
# @Date: 2019/9/17
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.step03_merge_all_sse_szse_stock_price_data
"""

import os

from tqdm import tqdm
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    sse_path = os.path.join(const.DATA_PATH, 'SSE_Stocks', '20120101_20190915_sh_stock')
    szse_path = os.path.join(const.DATA_PATH, 'SZSE_Stocks', 'sz_stock')

    for stock_path in [sse_path, szse_path]:
        file_list = os.listdir(stock_path)
        stock_df_list = []
        for f_name in tqdm(file_list):
            if not f_name.lower().endswith('.csv'):
                continue
            stock_df: DataFrame = pd.read_csv(os.path.join(stock_path, f_name), encoding='gbk',
                                              header=None, skiprows=1, dtype={const.DATE: str},
                                              names=[const.TRADING_SYMBOL, 'abbr', const.DATE, const.PRICE,
                                                     'Volume', 'Amount', 'price_chg', 'return', 'market_value',
                                                     'csho', '10'])
            stock_df.loc[:, const.DATE] = pd.to_datetime(stock_df[const.DATE], format='%Y%m%d')
            stock_df_list.append(stock_df)

        merged_df: DataFrame = pd.concat(stock_df_list, ignore_index=True, sort=False)
        merged_df.to_pickle(os.path.join(os.path.split(stock_path)[0], '20120101_20190915_stock_price.pkl'))
