# -*- coding: utf-8 -*-
import pandas as pd
from common import basefunc
from tradeTools import Decorator
import os
import copy
import better_exceptions
import sys
sys.path.append("./")
better_exceptions.hook()


class IndexData:
    # todo:akshare 数据不全
    def __init__(self):
        self._indexDfs = {}
        self._date_datas = {}
        self._pointer = 0

    def create(self, begin_date=19890101, indexSymbol="SH.000300"):
        self._date_datas = self.acquire_date_datas(indexSymbol)
        self.update(begin_date)

    def _load(self, indexID="000300"):
        workspace = basefunc.get_path_dirname()
        fileName = os.sep.join(
            [workspace, r"tradeTools", r"data",
             "IndexCons", f"{indexID}指数成分股数据.xlsx"])  #
        df = pd.read_excel(fileName, sheet_name="Sheet",
                           #    index_col=0, engine="openpyxl")
                           index_col=0)
        df.sort_index(ascending=True, inplace=True)
        df['date'] = pd.to_datetime(df.index, format='%Y-%m-%d')
        df.set_index('date', inplace=True)
        return df

    def getSymbols(self, dateTime: int, indexSymbol="SH.000300"):
        if indexSymbol not in self._indexDfs:
            self._indexDfs[indexSymbol] = self._load(indexID=indexSymbol[-6:])
        indexDF = self._indexDfs[indexSymbol]
        df = indexDF.iloc[indexDF.index <= str(dateTime)]
        symbols = []
        for index, row in df.iterrows():
            symbol = row["代码"][-2:] + "." + row["代码"][:6]
            addOrDel = row[r"纳入/剔除"]
            if addOrDel == "纳入":
                symbols.append(symbol)
            elif addOrDel == "剔除":
                symbols.remove(symbol)
            else:
                print(f"纳入/剔除 列的值错误 #{addOrDel}#")
        symbols.sort()
        return symbols

    # @Decorator._loadData(path="data")
    # def qryIndexStockCons(self,symbol = "SH.000300",**kwargs):
    #     import akshare as ak
    #     symbol = symbol[:2].lower()+symbol[-6:]
    #     index_stock_info_df = ak.index_stock_hist(index=symbol)
    #     return index_stock_info_df
    #
    # def getIndexCons(self,dateTime,symbol = "SH.000300"):
    #     cons = self.qryIndexStockCons(symbol = symbol)
    #     cons["tmp"] = cons["in_date"].astype(str)+cons["stock_code"].astype(str)
    #     cons = cons.drop_duplicates('tmp', 'first', ignore_index=True)
    #     cons["in_date"] = pd.to_datetime( cons["in_date"], format='%Y-%m-%d')
    #     cons["out_date"] = pd.to_datetime( cons["out_date"], format='%Y-%m-%d')
    #     into = cons[cons.in_date<=str(dateTime)]["stock_code"].tolist()
    #     print(len(into))
    #     print(into)
    #     ret =[]
    #     for _into in into:
    #         symbol = CodeFunc.add_prefix(_into)
    #         ret.append(symbol)
    #     ret.sort()
    #     print(ret)

    def acquire_date_datas(self, indexSymbol="SH.000300"):
        """构造以日期为 key 的字典"""
        if indexSymbol not in self._indexDfs:
            self._indexDfs[indexSymbol] = self._load(indexID=indexSymbol[-6:])

        datas = []
        symbols = []
        last_date = 0
        indexDF = self._indexDfs[indexSymbol]
        for index, row in indexDF.iterrows():
            date = index.year * 10000 + index.month * 100 + index.day

            if date != last_date or last_date == 0:
                last_date = date
                if len(symbols) > 0:
                    symbols = copy.copy(symbols)
                datas.append([last_date, symbols])

            symbol = row["代码"][-2:] + "." + row["代码"][:6]
            addOrDel = row[r"纳入/剔除"]

            if addOrDel == "纳入":
                symbols.append(symbol)
            elif addOrDel == "剔除":
                symbols.remove(symbol)
            else:
                print(f"纳入/剔除 列的值错误 #{addOrDel}#")

        return datas

    def update(self, current_date):
        assert (self._pointer >= 0 and self._pointer < len(self._date_datas))

        # 已经是最后的索引了
        if self._pointer == len(self._date_datas) - 1:
            return

        for idx in range(self._pointer, len(self._date_datas)):
            # 如果已经到达最后一个索引
            if idx == len(self._date_datas)-1:
                self._pointer = idx
                return

            # 如果刚好在正确区间，则更新并退出
            if current_date >= self._date_datas[idx][0]  \
                    and current_date < self._date_datas[idx + 1][0]:
                self._pointer = idx
                return

            # 如果日期在区间前，则不处理
            if current_date < self._date_datas[self._pointer][0]:
                return

            self._pointer = idx

    def acquire_datas_by_date(self, current_date):
        """获取当前日期的集合"""
        # 如果日期在所有区间前面，则返回空集
        if self._pointer == 0 and current_date < self._date_datas[self._pointer][0]:
            return []

        self.update(current_date)

        return self._date_datas[self._pointer][1]

    def acquire_all_codes(self):
        """获取历史上所有的id"""
        allcodes = []
        for date, vs in self.acquire_date_datas():
            allcodes.extend(vs)
        allcodes = list(set(allcodes))
        return allcodes


if __name__ == '__main__':
    # logging.basicConfig()
    # symbols500 = getIndexSymbols()
    # print(symbols500)
    # symbols300 = getIndexSymbols(indexID="000300")
    # print(symbols300)
    # d = list(set(symbols300)&set(symbols500))
    # print(len(d))
    idxData = IndexData()
    # idxData.qryIndexStockCons(symbol = "SH.000300")
    # r = idxData.getSymbols(dateTime = 20211222,indexSymbol = "SH.000852")
    # r = idxData.getSymbols(dateTime = 20211222,indexSymbol = "CSI.000825")
    r = idxData.getSymbols(dateTime=20220630, indexSymbol="SH.000852")
    print(len(r))
    print(r)
    # SH.689009
