# 从akshare 获取 ST 股票的简称变更信息
# 构造数数据结构，方便快速检查某个时间的 ST 股票

import datetime
import os
from typing import List

import akshare as ak
import pandas as pd
from common import basefunc

from tradeTools import helpers
from tradeTools.code_func import CodeFunc

class StockST:
    def __init__(self):
        self.st_info = {}

    def makeup_st_info(self):
        filename = 'data/stock_info_sz_change_name.csv'
        if not os.path.exists(filename) or datetime.date.fromtimestamp(os.path.getmtime(filename)) != datetime.date.today():
            stock_info_sz_change_name_df = ak.stock_info_sz_change_name(symbol="简称变更")
            stock_info_sz_change_name_df.to_csv(filename, index=False)

        df = pd.read_csv(filename)
        for _, row in df.iterrows():
            date, code, _, old_name, new_name = row
            date = int(date.replace('-', ''))
            code = CodeFunc.add_prefix(code)
            if 'ST' not in old_name and 'ST' in new_name:
                if code not in self.st_info:
                    self.st_info[code] = []
                self.st_info[code].append([date, None])
            elif 'ST' in old_name and 'ST' not in new_name:
                if code in self.st_info:
                    for info in self.st_info[code]:
                        if info[1] is None:
                            info[1] = date
                            break

    def is_stock_st(self, code, date):
        if code not in self.st_info:
            return False
        for start_date, end_date in self.st_info[code]:
            if end_date is None or start_date <= date <= end_date:
                return True
        return False

    def get_st_stocks(self, date):
        result = []
        for code, info in self.st_info.items():
            for start_date, end_date in info:
                if (end_date is None and date >= start_date)\
                    or start_date <= date <= end_date:
                    result.append(code)
                    break
        return result


_stock_st = StockST()
_stock_st.makeup_st_info()

# 检查某只股票某一日是否是ST
def is_stock_st(code: str, date: int) -> bool:
    return _stock_st.is_stock_st(code, date)

# 获取某一日的所有ST股票
def get_st_stocks(date: int) -> List[str]:
    return _stock_st.get_st_stocks(date)



@basefunc.timeit
def test():
    days = helpers.get_trading_days(19940101,20230630)
    for day in days:
        get_st_stocks(day)

if __name__ == '__main__':
    test()