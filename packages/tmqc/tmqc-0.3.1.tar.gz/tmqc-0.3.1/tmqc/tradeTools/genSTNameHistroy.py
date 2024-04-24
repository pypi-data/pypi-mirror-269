
import pandas as pd
import os
import json
from common import log
import requests
from common import basefunc

# warnings.simplefilter('ignore')

# realPathFile = (os.path.realpath(__file__))
base = basefunc.get_path_dirname()
ST_CONF_FILE = os.sep.join(
    [base, "tradeTools", "data", "SThistory", "SThistory.conf"])


def load(excel_name="全部A股"):
    # 加载手动下载的excel文件
    base = basefunc.get_path_dirname()
    excel_file = f"{excel_name}.xlsx"
    paths = [base,
             "tradeTools",
             "data",]
    if excel_name in ["退市资料", "已摘牌股票"]:
        paths.append("delisted")
    else:
        paths.append("SThistory")
    paths.append(excel_file)
    file_path = os.sep.join(paths)
    # 读取的df如果为空，需要手动保存下
    df = pd.read_excel(file_path, engine="openpyxl")
    # thresh=n是指：保留下来的每一行，其非NA的数目>=n。
    df.dropna(axis=0, thresh=2, inplace=True)
    return df


def gen():
    # 通过Choice导出的数据 获取带帽和摘帽时间点
    # 简称的变更通过wind获取，目前有部分数据有缺失，
    # 如果是带帽的名称丢失可以用st__替代。
    # *东财数据无法判断摘帽后是*st->st 还是直接摘
    # *目前通过wind的简称变更记录来匹配

    # !如果摘帽的名称数据丢失。因为不确定是否全摘
    delistDf = load(excel_name="已摘牌股票")
    listingDf = load(excel_name="全部A股")
    putStDf = load(excel_name="实施ST")
    cancelStDf = load(excel_name="撤销ST")
    delistInfoDf = load(excel_name="退市资料")

    if os.path.exists(ST_CONF_FILE):
        with open(ST_CONF_FILE) as f:
            total = json.load(f)
    else:
        total = {}

    concatDF = pd.concat([delistDf, listingDf])  # 退市及正常股票的摘帽记录合并
    delistSymbols = delistDf["证券代码"].tolist()
    for _, row in concatDF.iterrows():
        symbol = row["证券代码"]
        if symbol.startswith(("8", "9", "2")):  # 剔除北交所，B股
            continue

        if symbol in total and "delist" in total[symbol]:
            print(f"{symbol} 已退市不再增加更新")  # 退市股票不用再次更新数据
            continue

        if symbol not in total:
            total[symbol] = {}

        if symbol in delistSymbols:
            total[symbol]["delist"] = True
            # 退市日期
            _delistInfo = delistInfoDf[delistInfoDf["代码"] == symbol]
            if not _delistInfo.empty:
                delistDate = _delistInfo.iloc[0]["退市日期"].strftime("%Y-%m-%d")
                delistReason = _delistInfo.iloc[0]["终止上市原因"]
                total[symbol][delistDate] = {
                    "opt": "退市",
                    "newName": _delistInfo.iloc[0]["名称"],
                    "delistReason": delistReason

                }
                # 退市 有的股票是合并
                # if not _delistInfo.iloc[0]["重组后代码"].astype(str).strip()=='':
                if type(_delistInfo.iloc[0]["重组后代码"]) is str:
                    merge_code = _delistInfo.iloc[0]["重组后代码"]
                    total[symbol][delistDate]["merge"] = merge_code
            else:
                log.WriteLog("SThistory", f"{symbol}  找不到退市日期数据")

            # 获取退市整理日期
            # 在实施ST.xlsx 中会在名称最后加一个退字
            _putStDf = putStDf[(putStDf["代码"] == symbol) & (
                putStDf["实施后简称"].str.contains("退", na=False))]

            if _putStDf.empty:
                log.WriteLog("SThistory", f"{symbol}  找不到进入退市整理期数据")
            else:
                preDelistDate = _putStDf.iloc[0]["实施日期"].strftime("%Y-%m-%d")
                if preDelistDate in total[symbol]:
                    log.WriteLog("SThistory", f"{symbol}  退市整理期和退市日期重复")
                    continue
                total[symbol][preDelistDate] = {
                    "opt": "退市整理期",
                    "newName": _putStDf.iloc[0]["实施后简称"],
                    "delistReason": _putStDf.iloc[0]["实施ST原因"],
                }

        d = row["戴帽摘帽日期"]
        if d == "——":
            continue
        for _d in d.split(","):
            opt, dateTime = _d.split(":")
            if dateTime in total[symbol]:
                continue
            _querydf = cancelStDf if opt.startswith("去") else putStDf
            _queryName = "撤销后简称" if opt.startswith("去") else "实施后简称"
            _queryOptDateName = "撤销日期" if opt.startswith("去") else "实施日期"

            _put = _querydf[
                (_querydf["代码"] == symbol)
                & (_querydf[_queryOptDateName] == dateTime)
                & (_querydf["证券类型"] == "A股")
            ]
            if _put.empty:
                log.WriteLog(
                    "SThistory", f"{symbol} {opt} {dateTime} 找不到wind对应的名称变更记录")
            newName = _put.iloc[0][_queryName] if not _put.empty else f"{opt}__"
            total[symbol][dateTime] = {
                "opt": opt,
                "newName": newName

            }
            print(f"{symbol}增量更新{opt} {newName}")

    with open(ST_CONF_FILE, 'w') as f:
        f.write(
            json.dumps(total, indent=4, sort_keys=True,
                       ensure_ascii=False))
    return total


def updateCancelST():
    # 如果配置文件中 newName的值是"去*ST__" 表示摘帽后的名字未知是否还包含st。执行该方法来判别
    # https://data.eastmoney.com/notices/hsa/3.html
    # 读取东财网的公告通过名称来判断当时的名称是否包含st来辅助数据
    def _getData(chkdate, symbol):
        url = "https://np-anotice-stock.eastmoney.com/api/security/ann?"
        _params = {
            "sr": -1,
            "page_size": 1000,
            "page_index": 1,
            "ann_type": "A",
            "client_source": "web",
            "stock_list": symbol[:6],
            "f_node": 0,
            "s_node": 0,
        }
        for npage in range(1, 200):
            _params["page_index"] = npage
            text = requests.get(url, params=_params, timeout=30).text
            res = json.loads(text)

            data = []
            for d in res["data"]["list"]:
                data.append({
                    "notice_date": d["notice_date"],
                    "title": d["title"],

                })
            df = pd.DataFrame(data)
            df["notice_date"] = pd.to_datetime(
                df["notice_date"], format='%Y-%m-%d')
            chkdf = df[df["notice_date"] <= chkdate]
            # print(df["notice_date"].min())
            if not chkdf.empty:

                tmp = df[df["notice_date"] > chkdate]
                print("=========", chkdate, symbol, "=========",)
                print(tmp.iloc[-5:-1])
                print("===")
                print(chkdf.iloc[0:5])

                return tmp.iloc[-1].title
    with open(ST_CONF_FILE) as f:
        total = json.load(f)
    for _symbol, _data in total.items():
        for _dateTime, __data in _data.items():
            if _dateTime == "delist":
                continue
            # 对于去*ST无法确定具体名称的。用公告的数据来替换
            if __data["opt"] == "去*ST" and __data["newName"] == "去*ST__":
                v = _getData(chkdate=_dateTime, symbol=_symbol)
                newName = v.replace(" ", "")
                print(newName.find("ST"))
                if newName.find("ST") != -1:
                    fmt = newName[newName.find("ST"):newName.find("ST")+4]
                    newName = fmt
                print("newName", newName)
                total[_symbol][_dateTime]["newName"] = newName

                with open(ST_CONF_FILE, 'w') as f:
                    f.write(
                        json.dumps(total, indent=4, sort_keys=True,
                                   ensure_ascii=False))
                if newName.find("ST") == -1:
                    # 手动确认是否正常
                    return


if __name__ == '__main__':
    # print(load(excel_name="全部A股"))
    # print(load(excel_name="实施ST"))
    # print(load(excel_name="撤销ST"))
    # print(load(excel_name="退市资料"))
    # print(load(excel_name="已摘牌股票"))

    # print(pd.concat([df,df1]))
    # df = df[df["实施后简称"].str.contains("退",na=False)]
    # symbol = "300038.SZ"
    # putStDf = load(excelName="实施ST")
    # _putStDf = putStDf[(putStDf["代码"] ==symbol) & (putStDf["实施后简称"].str.contains("退",na=False))]
    # print(_putStDf)
    # updateCancelST()
    total = gen()
    # print(total)
