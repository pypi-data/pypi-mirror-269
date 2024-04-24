"""生成或者查询上市、退市日期
该方案是从K线表中取股票第一天日期，作为上市日期。取最后一天日期作为退市日期。
todo：缺陷是如果停牌的股票没有K线数据，则被认为是已经退市，如果策略以此判断而在“退市前”卖出，实际上是该股票停牌了，则会产生错误结果。
在回测系统底层 TradeBkt 中，可以配置是否提前自动平仓退市股票，具体处理在 process_delisting 中。
"""

import os
import re

from common import basefunc, log
from frame import DataContainer as DC
# from frame import DataType
# from frame.MarketContainer import StockContainer
from preprocess import gen_codes

# from collections import Counter

_K_data_table = 'tdx_day_data'


def get_kdata_last_date(database):
    """获得K线最后一条数据的日期"""
    sql = "SELECT time FROM %s ORDER BY TIME DESC LIMIT 1" % (_K_data_table)
    database.Query(sql)
    data = database.FetchOne()
    if not data: return None
    return data[0]

def get_listing_date(database, code):
    """获取指定股票的上市日期、退市日期"""
    sql = "SELECT time FROM %s WHERE code = '%s' ORDER BY TIME DESC LIMIT 1" % (_K_data_table, code)
    database.Query(sql)
    data = database.FetchOne()
    if not data: return None, None
    delisting_date = data[0]

    sql = "SELECT time FROM %s WHERE code = '%s' ORDER BY TIME ASC LIMIT 1" % (_K_data_table, code)
    database.Query(sql)
    data = database.FetchOne()
    listing_date = data[0]

    return listing_date, delisting_date

def acquire_listing_data(database, codes):
    """获取指定股票集合的上市、退市日期"""
    listing_dates =[]
    progress = 0
    last_date = 0
    length = len(codes)
    for code in codes:
        progress += 1
        listing_date, delisting_date = get_listing_date(database, code)
        if not listing_date:
            log.WriteLog("get_listing_err","get stock[%s] listing date fail from %s" % (code, _K_data_table))
            continue
        listing_dates.append((code, listing_date, delisting_date))
        last_date = max(last_date, delisting_date)
        print("std_listing_date: progress  %d/%d" % (progress, length) )

    return listing_dates, last_date

def gen(root):
    # 加载股票信息表
    database = basefunc.create_database()
    reQuery, stock_info = gen_codes.load_codes(root)
    codes = [si['code'] for si in stock_info]

    datas, last_date = acquire_listing_data(database, codes)

    # # 过滤掉抓取数据的最后一天，这一天不是退市日
    # dates = [d[1] for d in datas]
    # last_date = Counter(dates).most_common(1)[0][0]
    # datas = [(code, date) for code, date in datas if date != last_date]

    write_file(root, datas, last_date)
    return datas


def write_file(root, datas, last_date):
    """上市、退市数据写入文件"""
    filename = filename = os.path.join(root,'rec/listing_date.txt')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f'{last_date}\n')
        for code,listing_date,delisting_date in datas:
            f.write(f'{code}\t{listing_date}\t{delisting_date}\n')

def load_datas(database, root):
    """从文件中获取上市、退市日期数据"""
    filename = os.path.join(root,'rec/listing_date.txt')
    reQuery = False
    info = {}
    def append_info(e):
        info[e[0]] = ({'listing_date': e[1], 'delisting_date': e[2]})

    if os.path.exists(filename):
        with open(filename,'rt', encoding='utf8') as f:
            c = f.read()
            if len(c) > 0:
                ls = c.split('\n')
                last_date = ls[0]

                if last_date.isdigit() and get_kdata_last_date(database) <= int(last_date):
                    # 第一行记录的是日期，且该日期比数据库里最后一条记录更新
                    for l in ls[1:]:
                        try:
                            e = re.split(r'\s+', l)
                            if len(e) == 3:
                                append_info(e)
                        except:
                            pass
                    return reQuery, info

    """文件格式不对，或者数据不是最新，则重新生成"""
    reQuery = True
    datas = gen(root)
    info = {}
    for e in datas:
        append_info(e)
    return reQuery, info

if __name__ == '__main__':
    # gen()
    database = basefunc.create_database()
    reQuery, info = load_datas(database)
    print(info)