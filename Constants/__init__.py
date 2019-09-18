#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: __init__.py
# @Date: 2019/9/17
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

from .path_info import PathInfo, PROJECT_NAME


class Constants(PathInfo):
    PROJECT_NAME = PROJECT_NAME

    # Common Constants
    TRADING_SYMBOL = 'Symbol'
    EXCHANGE = 'Exchange'
    DATE = 'Date'
    YEAR = 'Year'
    MONTH = 'Month'
    PRICE = 'Price'
    RETURN = 'return'
    PRICE_CHANGE = 'price_chg'

    MARKET_VALUE = 'mkvalt'
    SHAREOUTSTANDING = 'csho'

    SSE = 'SSE'
    SZSE = 'SZSE'
    HKEX = 'HKEX'

    # CSMAR Related constants
    CSMAR_INT_ID = 'InstitutionID'
    CSMAR_SEC_ID = 'SecurityID'
