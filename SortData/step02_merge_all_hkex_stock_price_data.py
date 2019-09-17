#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_merge_all_hkex_stock_price_data
# @Date: 2019/9/17
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.step02_merge_all_hkex_stock_price_data
"""

import os

from tqdm import trange
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    hkex_path = os.path.join(const.DATA_PATH, 'HKEx_Stocks')

    hkex_dfs = []
    for start_year in trange(1980, 2017, 4):
        end_year = min([2019, start_year + 4])
        tmp_df: DataFrame = pd.read_csv(os.path.join(hkex_path, '{}09_{}09.txt'.format(start_year, end_year)),
                                        sep='\t', encoding='utf-16le')
        hkex_dfs.append(tmp_df)
    hkex_df: DataFrame = pd.concat(hkex_dfs, ignore_index=True, sort=False).drop_duplicates().rename(
        columns={'TradingDate': const.DATE})
    hkex_df: DataFrame = hkex_df.loc[hkex_df[const.DATE] != 'TradingDate'].copy()
    hkex_df.loc[:, const.DATE] = pd.to_datetime(hkex_df[const.DATE], format='%Y-%m-%d')
    hkex_df.to_pickle(os.path.join(hkex_path, '198009_201909_hkex_stock_information.pkl'))

