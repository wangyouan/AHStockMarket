#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_calculate_sh_sz_hk_stock_relative_index
# @Date: 2019/9/17
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.step01_calculate_sh_sz_hk_stock_relative_index
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    hsi_df: DataFrame = pd.read_excel(os.path.join(const.DATA_PATH, 'Stock Index Data.xlsx'), sheet_name='HSI')
    shci_df: DataFrame = pd.read_excel(os.path.join(const.DATA_PATH, 'Stock Index Data.xlsx'), sheet_name='SSE')
    szci_df: DataFrame = pd.read_excel(os.path.join(const.DATA_PATH, 'Stock Index Data.xlsx'), sheet_name='SZSE')

    hsi_useful: DataFrame = hsi_df.loc[:, ['Date', 'Price']].rename(columns={'Price': 'HSI'}).set_index('Date')
    shci_useful: DataFrame = shci_df.loc[:, ['Date', 'Price']].rename(columns={'Price': 'SHCI'}).set_index('Date')
    szci_useful: DataFrame = szci_df.loc[:, ['Date', 'Price']].rename(columns={'Price': 'SZCI'}).set_index('Date')

    merged_index_df: DataFrame = hsi_useful.merge(shci_useful, left_index=True, right_index=True).merge(
        szci_useful, left_index=True, right_index=True)

    ratio_df: DataFrame = merged_index_df / merged_index_df.iloc[0]
    fig = ratio_df.plot()

    merged_index_df.to_pickle(os.path.join(const.TEMP_PATH, '20190917_stock_index_data.pkl'))
    ratio_df.to_pickle(os.path.join(const.TEMP_PATH, '20190917_stock_index_ratio_data.pkl'))
