#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step05_get_connection_stock_index_data
# @Date: 2019/9/18
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.step05_get_connection_stock_index_data
"""

import os
import datetime

from tqdm import tqdm
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

STOCK_DATA_PATH = {
    const.SZSE: os.path.join(const.DATA_PATH, 'SZSE_Stocks', 'sz_stock', '20120101_20190915_stock_price.pkl'),
    const.SSE: os.path.join(const.DATA_PATH, 'SSE_Stocks', '20120101_20190915_sh_stock',
                            '20120101_20190915_stock_price.pkl'),
    const.HKEX: os.path.join(const.DATA_PATH, 'HKEx_Stocks', '198009_201909_hkex_stock_information2.pkl')
}

if __name__ == '__main__':
    connection_info_df: DataFrame = pd.read_csv(
        os.path.join(const.DATA_PATH, 'StockConnection', 'STK_MKTLink_StockInfo.txt'),
        sep='\t', encoding='utf-16le')

    connection_info_df_valid: DataFrame = connection_info_df.loc[connection_info_df['TradingStatusID'] == 'Q3401',
                                                                 ['Symbol', 'MarketLinkCode', 'ExchangeCode']]

    market_group = connection_info_df_valid.groupby('MarketLinkCode')

    target_date = datetime.datetime(2019, 8, 30)

    for linkage_code, link_df in tqdm(market_group):
        exchange_code = link_df.iloc[0]['ExchangeCode']
        if exchange_code == 'SZSE':
            price_file: DataFrame = pd.read_pickle(STOCK_DATA_PATH[const.SZSE]).rename(
                columns={'market_value': const.MARKET_VALUE})
            price_file.loc[:, const.TRADING_SYMBOL] = price_file[const.TRADING_SYMBOL].apply(
                lambda x: int(x.split('.')[0]))
        elif exchange_code == 'HKEX':
            price_file: DataFrame = pd.read_pickle(STOCK_DATA_PATH[const.HKEX]).rename(
                columns={'Amount': const.MARKET_VALUE})
        else:
            price_file: DataFrame = pd.read_pickle(STOCK_DATA_PATH[const.SSE]).rename(
                columns={'market_value': const.MARKET_VALUE})
            price_file.loc[:, const.TRADING_SYMBOL] = price_file[const.TRADING_SYMBOL].apply(
                lambda x: int(x.split('.')[0]))

        valid_price_file = price_file.loc[
            (price_file[const.DATE] == target_date) & (
                price_file[const.TRADING_SYMBOL].isin(set(link_df[const.TRADING_SYMBOL])))]
        print(linkage_code, valid_price_file[const.MARKET_VALUE].sum())
