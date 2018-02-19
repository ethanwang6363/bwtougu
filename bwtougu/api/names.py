#!/usr/bin/env python
# -*- coding: utf-8 -*-

VALID_HISTORY_FIELDS = [
    'datetime', 'open', 'close', 'high', 'low', 'total_turnover', 'volume',
    'acc_net_value', 'discount_rate', 'unit_net_value',
    'limit_up', 'limit_down', 'open_interest', 'basis_spread', 'settlement', 'prev_settlement'
]

VALID_GET_PRICE_FIELDS = [
    'OpeningPx', 'ClosingPx', 'HighPx', 'LowPx', 'TotalTurnover', 'TotalVolumeTraded',
    'AccNetValue', 'UnitNetValue', 'DiscountRate',
    'SettlPx', 'PrevSettlPx', 'OpenInterest', 'BasisSpread', 'HighLimitPx', 'LowLimitPx'
]

VALID_TENORS = [
    '0S', '1M', '2M', '3M', '6M', '9M', '1Y', '2Y', '3Y', '4Y',
    '5Y', '6Y', '7Y', '8Y', '9Y', '10Y', '15Y', '20Y', '30Y',
    '40Y', '50Y'
]

VALID_INSTRUMENT_TYPES = [
    'CS', 'Future', 'INDX', 'ETF', 'LOF', 'SF', 'FenjiA', 'FenjiB', 'FenjiMu',
    'Stock', 'Fund', 'Index'
]

VALID_XUEQIU_FIELDS = [
    'new_comments', 'total_comments',
    'new_followers', 'total_followers',
    'sell_actions', 'buy_actions',
]

VALID_MARGIN_FIELDS = [
    'margin_balance',
    'buy_on_margin_value',
    'short_sell_quantity',
    'margin_repayment',
    'short_balance_quantity',
    'short_repayment_quantity',
    'short_balance',
    'total_balance'
]

VALID_SHARE_FIELDS = [
    'total', 'circulation_a', 'management_circulation', 'non_circulation_a', 'total_a'
]

VALID_TURNOVER_FIELDS = (
    'today',
    'week',
    'month',
    'three_month',
    'six_month',
    'year',
    'current_year',
    'total',
)
