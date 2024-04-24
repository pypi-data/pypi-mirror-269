# -*- coding: utf-8 -*-
import bisect
import datetime
import json
import os
import re
import sys
from typing import List

import numpy as np
import pandas as pd
import requests
from common import basefunc

from tradeTools import Decorator
from tradeTools.code_func import CodeFunc

STOCK_CODE_PATH = 'stock_codes.conf'
# IDX_STOCKS={
# "HS300":"000300",
# "SZ50":"000016",
# "ZZ500":"000905"
# }


def get_stock_codes(real_time=False, stock_type=None, with_exchange=False):
    """获取所有股票 ID 到 all_stock_code 目录下
    real_time:是否实时
    stock_type:(fund 基金 stock 股票)
    with_exchange:是否要加上对应的证券市场编码
    """
    if real_time:
        all_stock_codes_url = 'http://www.shdjt.com/js/lib/astock.js'
        grep_stock_format = '~(\w+)`([^`]+)`'
        grep_stock_codes = re.compile(grep_stock_format)
        response = requests.get(all_stock_codes_url)
        # 这里对id去重
        stock_codes = list(set(grep_stock_codes.findall(response.text)))
        with open(stock_code_path(STOCK_CODE_PATH), 'w') as f:
            f.write(json.dumps(dict(stock=stock_codes), ensure_ascii=False))
    else:
        with open(stock_code_path(STOCK_CODE_PATH)) as f:
            stock_codes = json.load(f)['stock']

    if stock_type:
        stock_codes = [
            (stock[0], stock[1]) for stock in stock_codes if stock_type == CodeFunc.get_stock_type(stock[0])
        ]

    if with_exchange:
        stock_codes = [(CodeFunc.add_prefix(code[0]), code[1])
                        for code in stock_codes]

    return stock_codes


def get_codes_from_akshare(add_exchange=True):
    import akshare as ak
    df = ak.stock_info_a_code_name()
    stock_info = []
    for index, row in df.iterrows():
        code = row['code']
        if add_exchange:
            code = CodeFunc.add_prefix(code)
        name = row['name']
        stock_info.append({'code': code, 'name': name})
    return stock_info


def get_codes_from_web(filter_types: List[str] = ['stock', 'fund'],
                        use_akshare=True):
    if use_akshare:
        return get_codes_from_akshare()
    else:
        all_stock_codes_url = 'http://www.shdjt.com/js/lib/astock.js'
        grep_stock_format = r'~(\w+)`([^`\n]+?)(?:\.基金)*`'

        grep_stock_codes = re.compile(grep_stock_format)
        stock_info = []
        try:
            response = requests.get(all_stock_codes_url)
            found_info = grep_stock_codes.findall(response.text)
            stock_info = []
            last = 0
            for e in found_info:
                if e[0] == last:
                    continue
                if 'stock' in filter_types:
                    if e[0].startswith(
                            CodeFunc.SH_STOCK_PREFIX + CodeFunc.SZ_STOCK_PREFIX):
                        stock_info.append(
                            {'code': CodeFunc.add_prefix(e[0]), 'name': e[1]})
                        last = e[0]
                        continue
                if 'fund' in filter_types:
                    if e[0].startswith(CodeFunc.SH_FUND_PREFIX):
                        stock_info.append(
                            {'code': CodeFunc.add_prefix(e[0]), 'name': e[1]})
                        last = e[0]
                        continue
        except Exception as e:
            print(e)
        return stock_info


g_tdays = []
g_last_check = 0

def get_trading_days(from_date: int, to_date: int) -> List[int]:
    global g_tdays, g_last_check

    def _get_trading_days(from_date, to_date):
        url = f"http://113.31.125.219:8182/treading_days.php?from={from_date}&to={to_date}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(
                f"Request failed with status {response.status_code}")
        tdays = json.loads(response.text)
        return tdays

    # 没有数据，全量更新
    if len(g_tdays) == 0:
        _, today, _ = basefunc.get_today_date()
        g_tdays = _get_trading_days(from_date, today)

    # 数据少了，更新一下
    today = datetime.date.today()
    today_int = int(today.strftime('%Y%m%d'))  # 将today转换为整数类型
    holidays = [(1, 1), (5, 1), (10, 1)]  # 节假日列表，可以方便地添加更多节假日
    if today.weekday() < 5 and (today.month, today.day) not in holidays: #周末和节假日不更新
        if g_tdays[-1] < min(to_date, today_int):
            g_tdays.extend(_get_trading_days(g_tdays[-1], min(to_date, today_int)))

        if g_tdays[0] > from_date:
            before = _get_trading_days(from_date, g_tdays[0])
            before.extend(g_tdays)
            g_tdays = before

    idx_left = bisect.bisect_left(g_tdays, from_date)
    idx_right = bisect.bisect_right(g_tdays, to_date)
    return g_tdays[idx_left:idx_right]

# 生成调仓日
def generate_rebalance_days(from_date: int, to_date: int, interval: int) -> List[int]:
    trading_days = get_trading_days(from_date, to_date)
    rebalance_days = [trading_days[i]
                        for i in range(0, len(trading_days), interval)]
    return rebalance_days


def get_stock_codes_exclude_ST():
    all_stock_codes = get_stock_codes(
        real_time=True, stock_type="stock", with_exchange=False)  # 股票开板或者封板状态
    all_stock_codes = {int(s[0]): s[1] for s in all_stock_codes if
                        s[1].lower().find('st') == -1  # 过滤ST
                        and s[1].lower().find('pt') == -1
                        and s[1].lower().find('退') == -1
                        }  # 过滤ST
    return all_stock_codes


def stock_code_path(STOCK_CODE_PATH):
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
        paths = [base_dir, "tradeTools", STOCK_CODE_PATH]
        pathname = os.sep.join(paths)
    else:
        pathname = os.path.join(os.path.dirname(__file__), STOCK_CODE_PATH)
    print("pathname", pathname, "===============")
    return pathname

# 方便兼容打包exe


def get_path_dirname():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        # 取当前脚本的上级目录
        application_path = os.path.dirname(os.path.dirname(__file__))
    return application_path

# 回测 读取股票成交记录。提取买入股票清单


def get_buy_list_conf():
    path = ["conf", "buy_list.xlsx"]
    path = os.sep.join(path)
    work_dir = get_path_dirname()
    full_path = work_dir + os.sep + path
    buy_list = {}
    import xlrd

    # 1、打开文件
    with xlrd.open_workbook(full_path) as f:
        sheet = f.sheet_by_index(0)
        row_length = sheet.nrows  # 获取行长度
        for i in range(1, row_length):  # 过滤第一行标题
            data = sheet.row_values(i)
            _date = int(data[0])
            code = int(data[2])
            dir = data[4]
            if dir != "证券买入":
                continue
            if _date not in buy_list:
                buy_list[_date] = []
            buy_list[_date].append(code)

    return buy_list


def calc_time_diff(beg, end=None):
    b = datetime.datetime.strptime(str(beg), '%Y%m%d%H%M%S%f')
    if end:
        e = datetime.datetime.strptime(str(end), '%Y%m%d%H%M%S%f')
    else:
        e = datetime.datetime.now()
    seconds_diff = (e - b).total_seconds()
    return seconds_diff


def debug_data_print(data):
    _datetime = str(data['date']) + "%09d" % data['time']
    diff = calc_time_diff(_datetime)
    print('行情时间[%s]本机时间[%s]股票id[%s]与本机时间间隔[%s]'
          % (basefunc.format_datetime(_datetime),
                datetime.datetime.now(),
                data['code'],
                diff))


def debug_tran_print(data):
    trade_time = str(data['time'])
    _len = len(trade_time)
    today, _, _date = basefunc.get_today_date()
    if _len != 17:
        trade_time = _date + "%09d" % data['time']
    diff = calc_time_diff(trade_time)
    print('成交时间[%s]本机时间[%s]股票id[%06d]与本机时间间隔[%s]'
            % (basefunc.format_datetime("%09s" % data['time']),
            today,
            int(data['code']),
            diff))

    # 　上市公司季报披露时间：
    # 　　1季报：每年4月1日——4月30日。
    # 　　2季报（中报）：每年7月1日——8月30日。
    # 　　3季报： 每年10月1日——10月31日
    # 　　4季报 （年报）：每年1月1日——4月30日。
    # todo: 年报和一季度报最迟披露时间一致，默认返回年报


def getReportDate(dateTime: int, isUseYear=True):
    # isUseYear:True 返回年报日期 Fasle 返回一季度日期
    mmdd = dateTime % 10000
    year = dateTime // 10000
    dateRange = [1031, 830, 430, ]  # 公布日期

    reportDate = [930, 630, 1231] if isUseYear else [930, 630, 331,]
    for idx, _dateRange in enumerate(dateRange):
        if mmdd > _dateRange:
            if idx == 2:
                year = year - 1 if isUseYear else year
            return year * 10 ** 4 + reportDate[idx]
    return (year - 1) * 10 ** 4 + reportDate[0]


def get_half_report_date(date: int):
    # 依据最迟披露日期获取可得的半年报或年报日期
    date = datetime.datetime.strptime(str(date), '%Y%m%d')
    if date.month >= 9:
        return int(f'{date.year}0630')
    elif date.month >= 5:
        return int(f'{date.year-1}1231')
    else:
        return int(f'{date.year-1}0630')


def getTTmReportDates(reportDate):
    """返回一年滚动需要查询的报告期
        上年同季度日期，上年的年报日期，当季报告期

        如果reportDate是年报日期。则直接返回reportDate
    """
    quarterDate = reportDate % 10 ** 4
    if quarterDate == 1231:
        return [reportDate]
    lastYear = reportDate // 10 ** 4 - 1
    quarterDates = list(set([reportDate % 10 ** 4, 1231]))
    reportDates = [lastYear * 10 ** 4 + q for q in quarterDates]
    reportDates.append(reportDate)
    return reportDates


@Decorator.loadData()
def getSymbolsInfo(is_real_time=False,
                    parse_dates=["listingDate", "摘牌日期"],
                   **kwargs) -> pd.DataFrame:
    """生成 股票代码，名称，和行业 上市日期,一级行业代码,一级行业名称,摘牌日期
        https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/Index?type=web&code=SZ300059#
    Args:
        is_real_time (bool, optional): [如果为True，只会增量添加数据]. Defaults to False.

    Returns:
        pd.DataFrame: [ name                           object
                        industry                       object
                        listingDate            datetime64[ns]
                        industryNameLv1Code            object
                        industryNameLv1                object
                        摘牌日期                   datetime64[ns]]
    """

    fileName = kwargs["fileName"]
    stock_codes = get_codes_from_web(filter_types=['stock'])
    # use_akshare 没有退市股票，如果需要退市股票打开注释
    # stock_codes = get_codes_from_web(filter_types=['stock'],
    #                                  use_akshare=False)
    cathchedSymbols = []
    if os.path.exists(fileName):
        df = pd.read_csv(fileName, index_col=0,)
        df = df.dropna(subset=['listingDate'])  # 有些股票没有上市时间。删除后，继续尝试重新抓取
        cathchedSymbols = df.index.tolist()

    symbols = {_d["code"]: _d["name"] for _d in stock_codes}
    catchSymbols = list(set(symbols.keys())-set(cathchedSymbols))  # 需要增加的股票
    catchSymbols.sort()
    # https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/PageAjax?code=SZ301176
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/PageAjax?"
    params = {
        "code": "",
    }
    data = []
    i, cnt = 0, len(catchSymbols)
    industryEM = getEMindustryCode(is_real_time=is_real_time)
    for symbol in catchSymbols:
        i += 1
        print(f"{symbol} {symbols[symbol]}\t{i}/{cnt}")
        params["code"] = symbol.replace(".", "")
        r = requests.get(url, params=params)
        textData = r.text
        dataJson = json.loads(textData)
        if "status" in dataJson and dataJson["status"] == -1:
            print(f"{symbol} 无数据")
            continue
        # 未上市
        if "LISTING_DATE" not in dataJson["fxxg"][0] or not dataJson["fxxg"][0]["LISTING_DATE"]:
            print(f"{symbol} 可能未上市")
            continue
        industry = dataJson["jbzl"][0]["EM2016"]
        industryNameLv1 = industry.split("-")[0]  # 1级行业名称
        result = industryEM.loc[industryEM['所属东财行业(2016)\n1级']
                                == industryNameLv1, '所属东财行业(2016)代码\n1级']
        industryNameLv1Code = result.iloc[0]

        listingDate = pd.to_datetime(
            dataJson["fxxg"][0]["LISTING_DATE"]) if dataJson["fxxg"][0]["LISTING_DATE"] else np.nan
        series = pd.Series({"name": symbols[symbol],
                            "industry": industry,
                            "listingDate": listingDate,
                            "industryNameLv1Code": industryNameLv1Code,
                            "industryNameLv1": industryNameLv1,
                            }, name=symbol)
        data.append(series)
    if cathchedSymbols:
        # df = df.append(pd.DataFrame(data))
        df = pd.concat([df, pd.DataFrame(data)])
    else:
        df = pd.DataFrame(data)
    delisted_info = get_delisted_info(is_real_time=is_real_time)
    delisted_col_name = '摘牌日期'
    if delisted_col_name in df.columns:
        # 先删除delisted_col_name列
        df = df.drop(delisted_col_name, axis=1)
    df = df.merge(delisted_info[[delisted_col_name]],
                    left_index=True, right_index=True, how='left')
    return df


@Decorator.loadData(path="data")
def getKzzCodes(parse_dates=["上市时间"], **kwargs) -> pd.DataFrame:
    """获取可转债基础信息
    isRealTime: True 实时抓取 东财网数据  http://data.eastmoney.com/kzz/default.html
    Returns:
        pd.DataFrame: _description_
    """
    # =============akshare 数据提取不全。废弃=====================
    # import akshare as ak
    # df = ak.bond_zh_cov()
    # df["债券代码"] = df["债券代码"].apply(lambda x:f"SH.{x}" if str(x).startswith("11") else f"SZ.{x}")
    # df["正股代码"] = df["正股代码"].apply(lambda x:CodeFunc.add_prefix(x))
    # df["上市时间"].replace("-","",inplace=True)
    # df["上市时间"] = pd.to_datetime( df["上市时间"])
    # df = df.set_index("债券代码", verify_integrity=True)
    # return df
    # ==============================================================
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get?"
    cols = {
        "SECURITY_CODE": "债券编号",
        "SECUCODE": "债券代码",
        "SECURITY_NAME_ABBR": "债券简称",
        "CONVERT_STOCK_CODE": "正股代码",
        "SECURITY_SHORT_NAME": "正股简称",
        "LISTING_DATE": "上市时间",
        "DELIST_DATE": "退市日期",
    }
    fmtCols = ",".join(cols.keys())

    params = {
        "sortColumns": "SECURITY_CODE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_BOND_CB_LIST",
        # "columns": "ALL",  # ALL 参数返回所有提供的字段
        "columns": fmtCols,
        "source": "WEB",
        "client": "WEB",
        "quoteType": "0",
        "quoteColumns": "",
    }
    totalData = []
    for page in range(1, 10):
        params["pageNumber"] = page
        r = requests.get(url, params=params)
        data_json = json.loads(r.text)
        pages = data_json["result"]["pages"]
        data = data_json["result"]["data"]
        print(page, len(data))
        totalData.extend(data)
        if page == int(pages):
            break

    df = pd.DataFrame(data=totalData,)
    df.columns = list(cols.values())
    # # todo 过滤13开头的交换债
    df["symbol"] = df["债券编号"].apply(
        lambda x: f"SH.{x}" if str(x).startswith("11") else f"SZ.{x}")
    df["正股代码"] = df["正股代码"].apply(lambda x: CodeFunc.add_prefix(x))
    df = df.set_index("symbol", verify_integrity=True)
    # print(df)
    return df


@Decorator.loadData()
def getEMindustryCode(*args, **kwargs):
    # 东方1级行业码表
    total = []
    for excelName in ["全部A股行业列表.xlsx", "已摘牌股票行业列表.xlsx"]:
        base = basefunc.get_path_dirname()
        filepath = os.sep.join([base,
                                "tradeTools",
                                "data", "industry", excelName])
        indDf = pd.read_excel(filepath, sheet_name=0,
                                index_col=0, engine="openpyxl")
        indDf.index = indDf.index.map(
            lambda x: x.split(".")[1]+"."+x.split(".")[0])
        total.append(indDf)
    total = pd.concat(total)
    return total


@Decorator.loadData()
def get_delisted_info(*args, **kwargs):
    # 读取东财退市股票列表
    base = basefunc.get_path_dirname()
    excelName = "已摘牌股票.xlsx"
    filepath = os.sep.join([base,
                            "tradeTools",
                            "data", "delisted", excelName])
    df = pd.read_excel(filepath, sheet_name=0, index_col=0, engine="openpyxl")
    df.dropna(inplace=True)
    # 证券代码 转化
    df.index = df.index.map(lambda x: x.split(".")[1]+"."+x.split(".")[0])
    df["摘牌日期"] = pd.to_datetime(df["摘牌日期"])
    return df


if __name__ == '__main__':
    # 加载退市股票数据
    # df1 = get_delisted_info(is_real_time=True)
    # print(df1)
    # =================生成股票代码，名称，和行业 上市日期=============
    df = getSymbolsInfo(is_real_time=True)
    print(df)
    # print(df[df["摘牌日期"] <= "20230915"])
    # codes = get_codes_from_web()
    # print(len(codes))
    # print(codes)
