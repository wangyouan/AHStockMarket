#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step06_calculate_abnormal_return_of_event
# @Date: 2019/9/18
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.step05_get_connection_stock_index_data
"""

import os
import datetime

import numpy as np
from tqdm import tqdm
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const
from .step05_get_connection_stock_index_data import STOCK_DATA_PATH


def get_period(trading_days, event_date, period_start=0, period_end=5):
    if period_start > period_end:
        raise ValueError('Start day {} less than end day {}'.format(period_start, period_end))

    if period_start >= 0:
        return trading_days[trading_days >= event_date].iloc[period_start:period_end + 1]

    if period_end < 0:
        return trading_days[trading_days <= event_date].iloc[period_start - 1:period_end]

    if period_end == 0:
        return trading_days[trading_days <= event_date].iloc[period_start:]

    before_trading_days = get_period(trading_days, event_date, period_start, -1)
    after_trading_day = get_period(trading_days, event_date, 0, period_end)

    return pd.concat([before_trading_days, after_trading_day])


def get_cumulative_abnormal_return_of_specific_stocks(event_row, price_df, market_return):
    event_date = event_row[const.DATE]
    stock_symbol = event_row[const.TRADING_SYMBOL]
    target_stock_return = price_df.loc[price_df[const.TRADING_SYMBOL] == stock_symbol].copy()
    trading_days = market_return[const.DATE].sort_values(ascending=True)

    sample_period = get_period(trading_days, event_date, period_start=-20, period_end=20)

    result_dict = {}
    for i, j in enumerate(sample_period):
        result_dict['AR{}'.format(i - 20)] = np.nan

        day_market_return = market_return.loc[market_return[const.DATE] == j, 'mktret'].iloc[0]
        target_return = target_stock_return.loc[target_stock_return[const.DATE] == j]
        if target_return.empty:
            continue
        else:
            result_dict['AR{}'.format(i - 20)] = target_return[const.RETURN].iloc[0] - day_market_return

    return pd.Series(result_dict)


def get_cumulative_abnormal_return(connect_event, market_type):
    price_df = pd.read_pickle(STOCK_DATA_PATH[market_type]).loc[:, [const.TRADING_SYMBOL, const.DATE, const.RETURN]]

    if market_type != const.HKEX:
        price_df.loc[:, const.RETURN] = price_df[const.RETURN] / 100
        price_df.loc[:, const.TRADING_SYMBOL] = price_df[const.TRADING_SYMBOL].apply(lambda x: int(x.split('.')[0]))

    if market_type == const.SZSE:
        market_return: DataFrame = pd.read_csv(os.path.join(const.DATA_PATH, 'TRD_Dalym.txt'),
                                               sep='\t', encoding='utf-16le')
        market_return.loc[:, const.DATE] = pd.to_datetime(market_return['Trddt'], format='%Y-%m-%d')
        market_return: DataFrame = market_return.loc[market_return['Markettype'] == 4,
                                                     [const.DATE, 'Dretwdtl']].rename(columns={'Dretwdtl': 'mktret'})

    elif market_type == const.SSE:
        market_return: DataFrame = pd.read_csv(os.path.join(const.DATA_PATH, 'TRD_Dalym.txt'),
                                               sep='\t', encoding='utf-16le')
        market_return.loc[:, const.DATE] = pd.to_datetime(market_return['Trddt'], format='%Y-%m-%d')
        market_return: DataFrame = market_return.loc[market_return['Markettype'] == 1,
                                                     [const.DATE, 'Dretwdtl']].rename(columns={'Dretwdtl': 'mktret'})

    else:
        hsi_df: DataFrame = pd.read_excel(os.path.join(const.DATA_PATH, 'Stock Index Data.xlsx'), sheet_name='HSI')
        market_return: DataFrame = hsi_df.loc[:, [const.DATE, 'Change %']].rename(columns={'Change %': 'mktret'})

    event_with_car: DataFrame = connect_event.merge(
        connect_event.apply(get_cumulative_abnormal_return_of_specific_stocks, axis=1,
                            market_return=market_return, price_df=price_df),
        left_index=True, right_index=True)
    return event_with_car


if __name__ == '__main__':
    tqdm.pandas()
    event_df: DataFrame = pd.read_csv(os.path.join(const.DATA_PATH, 'StockConnection', 'STK_MKTLink_StockInfoChg.csv'),
                                      sep='\t', encoding='utf-16le').replace({'调入': 'in', '调出': 'out'})
    event_df.loc[:, const.DATE] = pd.to_datetime(event_df['ChangeDate'], format='%Y-%m-%d')
    hk_related_events = event_df.loc[event_df['MarketLinkCode'].isin(
        {'HKEXtoSZSE', 'HKEXtoSSE'}), ['Symbol', 'ChangeType', const.DATE]].drop_duplicates()
    sse_related_events = event_df.loc[event_df['MarketLinkCode'] == 'SSEtoHKEX',
                                      ['Symbol', 'ChangeType', const.DATE]].copy()
    szse_related_events = event_df.loc[event_df['MarketLinkCode'] == 'SZSEtoHKEX',
                                       ['Symbol', 'ChangeType', const.DATE]].copy()

    hk_ar_return = get_cumulative_abnormal_return(hk_related_events, const.HKEX)
    sh_ar_return = get_cumulative_abnormal_return(sse_related_events, const.HKEX)
    sz_ar_return = get_cumulative_abnormal_return(szse_related_events, const.HKEX)

    hk_ar_return.to_pickle(os.path.join(const.TEMP_PATH, '20190919_hk_listed_stock_ar_returns.pkl'))
    sh_ar_return.to_pickle(os.path.join(const.TEMP_PATH, '20190919_sh_listed_stock_ar_returns.pkl'))
    sz_ar_return.to_pickle(os.path.join(const.TEMP_PATH, '20190919_sz_listed_stock_ar_returns.pkl'))
