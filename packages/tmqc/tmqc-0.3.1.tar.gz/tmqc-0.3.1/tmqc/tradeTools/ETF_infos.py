# -*- coding: utf-8 -*-
from re import sub
from tradeTools.code_func import CodeFunc
from common import log
from common.define import SUBSTITUTE_FLAG
from common import basefunc
import json
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

SETTING = basefunc.get_strategy_setting()
FILENAME = "按照清单净值计算_%s"


class ETF_Info:
    def __init__(self, date_time):
        # self.dc = data_center.use()
        self.etf_infos = self.load(date_time=date_time)

    def load(self, date_time: int):
        self.date_time = date_time

        etf_infos = {}
        path = os.sep.join([basefunc.get_path_dirname(),
                           "conf", "etf", str(date_time // 100)])
        if not os.path.exists(path):
            txt = "不存在该路径{}".format(path)
            print(txt)
            return etf_infos
        full_paths = [os.sep.join([path, "etf_%s_%s.conf" % (
            market_name, date_time)]) for market_name in ["sh","sz", ]]

        for full_path in full_paths:
            if not os.path.exists(full_path):
                print("未找到etf配置路径 ", full_path)
                continue
            if os.stat(full_path).st_size == 0:
                # 文件为空，不进行读取操作
                print(f"{full_path}无数据")
                obj = None
            else:
                with open(full_path, 'rb') as f:
                    import chardet
                    result = chardet.detect(f.read())
                    print(full_path)
                    print(result)
                # with open(full_path, encoding='CP1252') as f:
                with open(full_path, encoding='utf8') as f:
                    # position = 108561
                    # f.seek(max(0, position - 3))
                    # print(f.read(2))  # 打印出该位置前面的字符
                    obj = json.load(f)
                    for fundid2, details in obj.items():
                        constituent_stock_info = {
                            int(stock_id): v for stock_id, v in details["constituent_stock_info"].items()}
                        details["constituent_stock_info"] = constituent_stock_info
                        etf_infos.update(
                            {CodeFunc.add_prefix(fundid2): details})
            print("读取etf配置路径 ", full_path)
        return etf_infos

    def get_creationRedemptionUnit(self, fundid2) -> int:
        """申赎单位(份)"""
        return int(self.etf_infos[fundid2]["creationRedemptionUnit"])

    def get_estimatedCashComponent(self, fundid2) -> float:
        """预估现金"""
        # estimatedCashComponent = float(sub(r'[^-?\d.]', '', ))
        return self.etf_infos[fundid2]["estimatedCashComponent"]

    def get_constituent_stock_info(self, fundid2) -> dict:
        """成分股"""
        d = {CodeFunc.add_prefix(
            code): info for code, info in self.etf_infos[fundid2]["constituent_stock_info"].items()}
        return d

    def get_idx(self, fundid2) -> int:
        """跟踪指数"""
        return int(self.etf_infos[fundid2]["index_id"])

    def getRedemptionUnitAssetValue(self, fundid2) -> float:
        """上一个交易日的单位资产净值"""
        return float(self.etf_infos[fundid2]["fRedemptionUnitAssetValue"])

    def get_market_type(self, fundid2) -> int:  # 十位：（1:沪市 2:深市） 个位（2;跨市）
        """市场类型标志"""
        return int(self.etf_infos[fundid2]["market_type"])


if __name__ == '__main__':
    etf = ETF_Info(date_time=20231211)
    # fundid2 ="SH.512100"
    # print(etf.get_idx(fundid2="SH.512100"))
    k = etf.get_constituent_stock_info(fundid2="SZ.159601")
    print(len(k.keys()))
