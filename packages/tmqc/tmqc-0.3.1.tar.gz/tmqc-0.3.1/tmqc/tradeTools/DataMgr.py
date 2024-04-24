# -*- coding: utf-8 -*-
from tradeTools import helpers
from tradeTools import Decorator
from frame import data_center  # frame 软连接到trade模块的frame
from frame import stock_func
from datetime import datetime
import pandas as pd
import numpy as np
import os
import json
import re
import requests
from sqlalchemy import text
import demjson
from pyecharts.charts import Bar, Line, Grid
from pyecharts import options as opts
from pyecharts.charts import Scatter
from pyecharts.commons.utils import JsCode
from typing import List
from pandas import Series
from enum import Enum, auto
import bisect
from common import log


class AdjFrequency(Enum):  # 调仓频率
    DAILY = 1  # 日频，1日
    WEEKLY = 5  # 周频，5日
    MONTHLY = 21  # 月频，21日
    CUSTOM = 0  # 自定义


class Mgr():
    def __init__(self):
        self.oldDc = data_center.use()
        self.all_chg_days: list[int] = []
        self.last_chg_date = 0
        self.open_weight = pd.DataFrame(index=[], columns=['weight'])
        self.log_file = "trace"
    # @Decorator.loadData(path="data")

    def getST(self, dateTime=20210101, is_real_time=False, **kwargs):
        # 获取时点的st股票
        _dirPath = (os.path.dirname(__file__))
        fileName = os.sep.join(
            [_dirPath, r"data", "SThistory", "SThistory.conf"])
        with open(fileName) as f:
            total = json.load(f)

        stSymbols = {}
        for _symbol, data in total.items():
            _data = data.copy()
            if "delist" in _data:
                del _data["delist"]
            df = pd.DataFrame(_data).T
            df.index = pd.to_datetime(df.index)
            df = df[df.index <= str(dateTime)]
            if df.empty:
                continue
            df.sort_index(ascending=False, inplace=True)
            opt = df.iloc[0]["opt"]
            newName = df.iloc[0]["newName"]
            if opt in ["*ST", "ST"] or re.search("ST|退", newName):
                __symbol = _symbol.split(".")[1]+"."+_symbol.split(".")[0]
                stSymbols[__symbol] = {"newName": newName, "opt": opt}
        return pd.DataFrame(stSymbols).T

    # 获取上市满1年的股票
    # 过滤st股
    def getSymbols(self, dateTime=20210101,
                   years=-1,
                   isFilterSt=True,
                   is_real_time=False) -> pd.DataFrame:
        """读取满足设置条件的股票列表

        Args:
            dateTime (int, optional): _description_. Defaults to 20210101.
            years (int, optional): 上市时间约束，默认满一年. Defaults to -1.
            isFilterSt (bool, optional): 是否过滤st股, Defaults to True.
            is_real_time (bool, optional): _description_. Defaults to False.

        Returns:
            pd.DataFrame: _description_
        """
        if not hasattr(self, 'listDf') or is_real_time:
            self.listDf = helpers.getSymbolsInfo(is_real_time=is_real_time)
            listDf = self.listDf
        else:
            listDf = self.listDf
        start = datetime.strptime(
            str(dateTime), '%Y%m%d') + pd.tseries.offsets.DateOffset(years=years)
        symbols = listDf[listDf.listingDate <= str(start)].index.tolist()
        if isFilterSt:
            symbols = list(
                set(symbols) - set(self.getST(dateTime=dateTime).index.tolist()))

        # 北交所先过滤
        symbols = [symbol for symbol in symbols if not symbol.startswith('BJ')]
        return listDf.loc[symbols]

    @Decorator.firstLoad
    @Decorator.loadData(path="data")
    def gen_idx_data(self, index_symbol, is_real_time=False, **kwargs):
        if not hasattr(self, "oldDc"):
            self.oldDc = data_center.use()
        maxDate = 0
        fileName = kwargs["fileName"]
        if os.path.exists(fileName):
            oldDf = pd.read_csv(fileName, index_col=0,)
            maxDate = oldDf["time"].max()
        sql = "SELECT code,time,close from `index_day_data` "
        sql += f"WHERE code = '{index_symbol}'"
        if maxDate:
            sql += f" and time>{maxDate}"
        df = pd.read_sql(sql, self.oldDc.database.conn)
        if df.empty:
            return oldDf
        df['date'] = pd.to_datetime(df['time'], format='%Y%m%d')
        df.set_index('date', inplace=True)

        if maxDate:
            df = pd.concat([oldDf, df])
        df[index_symbol] = df.close / df.close.shift(1) - 1
        return df

    @Decorator.firstLoad
    @Decorator.loadData(path="data")
    def genSymbolRateData(self, symbol, is_real_time=True, **kwargs):
        # 生成间隔数据收益率数据
        if not hasattr(self, "oldDc"):
            self.oldDc = data_center.use()
        maxDate = 0
        fileName = kwargs["fileName"]
        if os.path.exists(fileName):  # 读取已有数据文件
            if os.stat(fileName).st_size == 0:
                oldDf = pd.DataFrame()
            else:
                oldDf = pd.read_csv(fileName, index_col=0,)
            # if not oldDf.empty:
                maxDate = oldDf["time"].max()
        # 多取一条历史数据为了算当日收益率
        sql = "SELECT code,time,close,volume "
        if symbol[-6:].startswith("1"):
            sql += f"from `bond_day_data` WHERE code = '{symbol}'"
        else:
            sql += f"from `tdx_day_data` WHERE code = '{symbol}'"
        if maxDate:
            sql += f" and time >={maxDate}"
        # 使用text函数将SQL语句包装为一个可执行对象
        sql = text(sql)
        df = pd.read_sql(sql, self.oldDc.database.conn)
        if df.empty:
            if maxDate:
                return oldDf
            return pd.DataFrame()

        df['date'] = pd.to_datetime(df['time'], format='%Y%m%d')
        df.set_index('date', inplace=True)

        df["lastTime"] = df.time.shift()
        df["lastClose"] = df.close.shift()

        def _getRehabilitationClose(hang):  # 复权
            begTime = hang.lastTime
            endTime = hang.time
            symbol = hang.code
            dividends = self.oldDc.query_dividends(stock_id=symbol,
                                                   begtime=begTime,
                                                   endtime=endTime)
            pre_close = hang.lastClose
            if dividends[symbol]:
                for dividend in dividends[symbol]:
                    pre_close = stock_func.get_dividend_pre_price(
                        pre_close, dividend[1])  # 前复权
            return (hang.close / pre_close) - 1

        df["rate"] = df.apply(_getRehabilitationClose, axis=1)
        if maxDate:
            df = df[df.time > maxDate]
            df = pd.concat([oldDf, df])
            df['date'] = pd.to_datetime(df['time'], format='%Y%m%d')
            df.set_index('date', inplace=True)
        return df

    # @Decorator.loadData(path="data")
    # def genSymbolTScore(self, symbol, frequency, windows,):  # 滚动z分数
    #     allData = self.genSymbolRateData(symbol=symbol, frequency=frequency)
    #     if allData.empty:
    #         return pd.DataFrame()
    #     allData['mRate'].fillna(0, inplace=True)  # 停牌的日期。收益率为设为0
    #     allData['mean'] = allData['mRate'].rolling(windows).mean()
    #     allData['std'] = allData['mRate'].rolling(windows).std(ddof=1)
    #     allData["ZScore"] = (allData['mRate'] - allData['mean'])/allData['std']
    #     allData["TScore"] = 50+10*allData["ZScore"]
    #     return allData[['mRate', 'mean', 'std', 'ZScore', 'TScore']]

    # def genTradeDays(self, begTime: int, frequency: int = 20, is_real_time=False):
    #     # todo resample
    #     # 根据换仓频率生成交易日列表
    #     # frequency 交易日间隔
    #     df = self.genIDXData(indexSymbol="SH.000001",
    #                          is_real_time=is_real_time)
    #     df = df[df.index >= str(begTime)]

    #     return df.iloc[0::frequency]

    def getSymbolRateData(self, symbol, is_real_time=False):
        if not hasattr(self, 'symbolRateData'):
            self.symbolRateData = {}
        if symbol not in self.symbolRateData:
            symbolRateData = self.genSymbolRateData(symbol=symbol,
                                                    is_real_time=is_real_time)
            if symbolRateData.empty:
                print(f"{symbol}无历史行情数据")
            self.symbolRateData[symbol] = symbolRateData
        return self.symbolRateData.get(symbol)

    # def getSymbolsData(self, symbols, endDate):
    #     rates = []
    #     marketValues = []
    #     for symbol in symbols:
    #         rateDf = self.genSymbolRateData(symbol=symbol)
    #         star = endDate.replace(endDate.year - 2)
    #         df = rateDf[(star <= rateDf.index) & (rateDf.index <= endDate)]
    #         rate = df["mRate"]
    #         marketValue = df["MarketV"]
    #         rate.name = symbol
    #         marketValue.name = symbol
    #         rates.append(pd.DataFrame(rate))
    #         marketValues.append(pd.DataFrame(marketValue))
    #     symbolsReturn = pd.concat(rates, axis=1)
    #     marketValue = pd.concat(marketValues, axis=1)
    #     marketValue["TOTAL"] = marketValue.sum(axis=1)
    #     marketValue = (marketValue.T / marketValue.TOTAL).T  # 求权重
    #     marketValue = marketValue.iloc[-1]
    #     marketValue = marketValue.drop("TOTAL")
    #     return symbolsReturn, marketValue

    def gen_return(self,
                   weight_date: int,
                   date_time: int,
                   symbols: list,
                   weight: list = []) -> float:
        """计算date_time当日持仓的收益率

        Args:
            weight_date (int): 生成初始权重的日期
            date_time (int): _description_
            symbols (list): _description_
            weight (list, optional): 初始权重列表. Defaults to [].

        Returns:
            float: _description_
        """

        rate: List[Series] = []
        for symbol in symbols:
            df = self.genSymbolRateData(symbol=symbol, is_real_time=True)
            # 读取个股的区间收益率
            s = df.loc[(str(weight_date) < df.index) & (
                df.index <= str(date_time))]["rate"]
            s.name = symbol
            rate.append(s)
        if not rate:
            return 0
        rateDf = pd.concat(rate, axis=1)
        rateDf = rateDf.fillna(0)  # 停牌股。当日的收益率为0
        if rateDf.shape[0] <= 1:
            rate = np.dot(rateDf.iloc[-1], weight)
        else:
            # 如果包含多个交易日。由初始交易日的权重和前一日的净值。得出前一日的权重比例。再和当日的收益率点积
            cumprodDf = (1 + rateDf).cumprod()
            # 考虑如果总仓位累加不为1
            _p = 1 - np.sum(weight)  # 初始留存的净值
            # 当前净值
            rate = _p+np.dot(cumprodDf.iloc[-1], weight)
            # 当前净值/上一日净值
            rate /= _p + np.dot(cumprodDf.iloc[-2], weight)
            rate -= 1
        return rate

    def get_open_weight(self, date_time, **kwargs) -> pd.DataFrame:
        """自定义调仓日 生成股票权重的方法

        Args:
            date_time (_type_): 调仓日

        Returns:
            pd.DataFrame: pd.DataFrame(index=[symbols], columns=['weight'])
        """

        pass

    def gen_chg_days(self, beg, adj_freq: AdjFrequency):
        # 如果adj_freq是AdjFrequency.CUSTOM。子类自行实现
        if self.all_chg_days:
            return self.all_chg_days
        assert adj_freq != AdjFrequency.CUSTOM, "子类需要实现该方法"
        idx_data = self.gen_idx_data(
            index_symbol="SH.000001", is_real_time=True)
        trade_days = idx_data[idx_data.index >= str(beg)]
        return trade_days.iloc[0::adj_freq.value].time.tolist()

    def update_or_keep_open_weight(self,
                                   date_time,
                                   **kwargs) -> list[int, pd.DataFrame]:
        """查找 小于等于 date_time 最近一个调仓日
        返回调仓日和权重信息

        Args:
            date_time (_type_): _description_

        Returns:
            list[int,pd.DataFrame]: 调仓日和权重信息
        """
        #
        index = bisect.bisect_right(self.all_chg_days, date_time)
        if index:
            last_chg_date = self.all_chg_days[index-1]
            if self.last_chg_date != last_chg_date:
                self.last_weight = self.get_open_weight(
                    date_time=last_chg_date, **kwargs)
                self.last_chg_date = last_chg_date
                txt = f"调仓日[{last_chg_date}]"
                txt += f"股票数量[{len(self.last_weight)}]"
                txt += f"前面3名[{self.last_weight.head(3).to_string(index=False)}]"
                log.WriteLog(self.log_file, txt)
        return self.last_chg_date, self.last_weight

    @Decorator.loadData()
    def gen_daily_net(self,
                      beg: int,
                      adj_freq: AdjFrequency,
                      index: str = "SH.000001",  # 基准指数
                      **kwargs) -> pd.DataFrame:
        """生成每日净值数据

        Args:
            beg (int): 策略开始日期
            adj_freq (AdjFrequency): 调仓日设置
            index (str, optional): 基准指数. Defaults to "SH.000001".
            kwargs : 可以配置get_open_weight 的传参
        Returns:
            pd.DataFrame: _description_
        """
        # 如果已有文件，增量更新净值
        old_file_path = kwargs["fileName"]
        old_total = pd.DataFrame()
        if os.path.exists(old_file_path):
            old_total = pd.read_csv(old_file_path, index_col=0,)
            old_total.index = pd.to_datetime(old_total.index)
            # last_traday = old_total.iloc[-1].name.strftime("%Y%m%d")

        self.all_chg_days = self.gen_chg_days(beg=beg, adj_freq=adj_freq)
        idx_data = self.gen_idx_data(
            index_symbol=index, is_real_time=True)
        idx_beg = beg if old_total.empty else old_total.index[-1].strftime(
            "%Y%m%d")
        # 生成全部交易日或者需要增量交易日
        trade_days = idx_data[idx_data.index >= str(idx_beg)].time.tolist()
        total = []  # 每日收益率
        _cnt_days = len(trade_days)
        for _idx, tradeDay in enumerate(trade_days):
            if _idx == 0:
                continue
            weight_date, last_weight = self.update_or_keep_open_weight(
                date_time=trade_days[_idx-1], **kwargs)
            ret = self.gen_return(
                weight_date=weight_date,
                date_time=tradeDay,
                symbols=last_weight.index.tolist(),
                weight=last_weight["weight"].tolist())
            print(f"{_idx}/{_cnt_days} {tradeDay} 收益率: {ret} ")
            total.append(
                pd.Series({"return": ret},
                          name=pd.to_datetime(tradeDay, format='%Y%m%d')))
        total = pd.DataFrame(total)
        total = pd.concat([total, idx_data[[index]]],
                          axis=1, join='inner', )

        if not old_total.empty:
            old_total = old_total.loc[:, ["return", index]].copy()
            total = pd.concat([old_total, total])

        cumprod = (1+total).cumprod()
        total = pd.concat([total, cumprod], axis=1, join='inner', )
        return total
    # 计算symbols组合的收益率

    def genReturnMonthlys(self, dateTime, symbols, frequency, ):
        seriseMonthRate = []
        for symbol in symbols:
            if not hasattr(self, 'symbolRateData'):
                self.symbolRateData = {}

            if symbol not in self.symbolRateData:
                symbolRateData = self.genSymbolRateData(symbol=symbol, frequency=frequency,
                                                        is_real_time=False)
                if symbolRateData.empty:
                    continue
                symbolRateData["lastMarketV"] = symbolRateData["MarketV"].shift()
                symbolRateData['lastMarketV'].fillna(
                    method='ffill', inplace=True)  # ’ffill’，向前填充，或是向下填充
                self.symbolRateData[symbol] = symbolRateData
            df = self.symbolRateData.get(symbol)

            if dateTime not in df.index:
                print(f"{symbol} {dateTime}的数据为空 ")
                continue
            s = df.loc[dateTime]
            seriseMonthRate.append(s)
        monthDf = pd.DataFrame(seriseMonthRate)
        if monthDf.empty:
            return monthDf
        monthDf["市值权重"] = monthDf.lastMarketV / monthDf.lastMarketV.sum()
        monthDf["wRate"] = monthDf.mRate * monthDf["市值权重"]  # 加权收益率
        print(monthDf)
        sumWRate = monthDf.wRate.sum()
        meanRate = monthDf.mRate.mean()
        returnMonthlyDf = pd.DataFrame([[sumWRate, meanRate]], index=[
                                       dateTime], columns=['sumWRate', "meanRate"])
        return returnMonthlyDf

    @Decorator.loadData()
    def get_report(self,
                   df: pd.DataFrame,
                   report_name,
                   index_symbol="",
                   **kwargs) -> pd.DataFrame:
        # df 每一列为每日收益率序列
        # index_symbol 基准指数
        # 生成净值图。夏普率等信息
        beg_time = df.iloc[0].name  # 策略开始时间
        end_time = df.iloc[-1].name  # 策略开始时间
        print(f"beg{beg_time} ,end{end_time}")
        if index_symbol:

            idx = self.gen_idx_data(index_symbol=index_symbol)
            idx = idx[(idx.index >= str(beg_time)) & (
                idx.index <= str(end_time))]
            idx = idx.loc[:, [index_symbol]]
            #  df中每个列减去指数日收益
            alpha = df.sub(idx[index_symbol], axis=0)
            # 给每列列名加上后缀 '_alpha'
            alpha = alpha.add_suffix('_alpha')
            # 每日收益率 加指数 加alpha
            df = pd.concat([df, idx, alpha], axis=1, join='outer', )
        tradays = df.shape[0]
        cumprod = (1+df).cumprod()
        # 最新累计净值
        last_net_value = pd.Series(cumprod.iloc[-1], name="last_net_value")
        # 年化收益率
        annual_return = pow(cumprod.iloc[-1], 252/tradays)-1
        annual_return = pd.Series(annual_return*100, name="annual_return(%)")
        # 最大回撤
        maximum_drawdown = 1-cumprod/np.maximum.accumulate(cumprod)
        report = pd.DataFrame(columns=cumprod.columns)
        report.loc["last_net_value"] = last_net_value
        report.loc["annual_return(%)"] = annual_return
        report.loc["maximum_drawdown"] = maximum_drawdown.max()
        std = df.std()
        year_std = std * pow(252, 0.5)
        # 夏普率
        sharp = annual_return/100/year_std
        report.loc["year_std"] = year_std
        report.loc["sharp"] = sharp

        # 生成净值图
        xaxis = [i.strftime("%Y%m%d") for i in cumprod.index.tolist()]
        line = Line().add_xaxis(xaxis)

        for col in cumprod.columns:
            line.add_yaxis(series_name=f"{col}",
                           y_axis=cumprod[col].tolist(),
                           )
            line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        min_val = cumprod.min().min()*0.9
        max_val = cumprod.max().max()*1.1
        line.set_global_opts(yaxis_opts=opts.AxisOpts(
            min_=min_val, max_=max_val))
        line.set_global_opts(
            legend_opts=opts.LegendOpts(pos_top='1%'),
        )
        line.set_series_opts(z=100)  # 线性图在柱形图之上

        bar = Bar().add_xaxis(xaxis)

        # bar.extend_axis(
        #     yaxis=opts.AxisOpts(
        #         name='最大回撤',
        #         type_='value',
        #         position='right'
        #     )
        # )
        # for col in maximum_drawdown.columns:
        #     bar.add_yaxis(series_name=f"{col}_mdd",
        #                   y_axis=maximum_drawdown[col].tolist(),
        #                   yaxis_index=1,
        #                   )
        #     bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False),
        #                         # itemstyle_opts={"margin_bottom":"30%"}
        #                         )
        # bar.set_global_opts(legend_opts=opts.LegendOpts(pos_top='bottom'))
        # bar.set_global_opts(legend_opts=opts.LegendOpts(pos_left="left"))
        # bar.set_global_opts(
        #     legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=10)),
        #     )
        bar.overlap(line)
        # bar.render()
        # todo grid 方式可以调整图例和表的相对位置防止重叠。但是次坐标轴不显示
        # 用于显示多个线性图
        grid = Grid()
        if index_symbol:
            grid.add(bar, grid_opts=opts.GridOpts(pos_top="20%"))
        else:
            grid.add(line, grid_opts=opts.GridOpts(pos_top="20%"))

        grid.render(f"{report_name}.html")
        return report

    def draw_scatter(self, dfs, name="tmp"):
        # 刻画散点图。df的前两行为xy轴。列名为散点名称
        js_code_str = '''
            function(params){
            return params.data[2];
            }
            '''
        # df = df.T
        # df = df.sort_values(by=df.columns[0])
        # df = df.T
        # print(df)

        # 创建散点图
        scatter = Scatter()
        import matplotlib.pyplot as plt
        import numpy as np

        def generate_colors(n: int):
            cmap = plt.get_cmap("hsv")
            colors = cmap(np.linspace(0, 1, n))
            return colors

        colors = generate_colors(len(dfs))

        # colors = ["blue", "red"]
        for i, df in enumerate(dfs):
            x_data = df.iloc[0].tolist()
            y_data = df.iloc[1].tolist()
            name_data = df.columns.tolist()
            print(x_data)
            print(y_data)
            data = [list(z) for z in zip(y_data, name_data)]
            # name_data 是每个散点的悬浮提示
            scatter.add_xaxis(x_data)
            scatter.add_yaxis(df.name,  # df.name 作为标签名称
                              data,
                              label_opts=opts.LabelOpts(is_show=False),
                              itemstyle_opts=opts.ItemStyleOpts(
                                  color=colors[i])
                              )

        # 设置全局配置项
        scatter.set_global_opts(
            # title_opts=opts.TitleOpts(title="Scatter Example"),
            xaxis_opts=opts.AxisOpts(
                name=df.iloc[0].name,
                type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                name=df.iloc[1].name,
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(formatter=JsCode(js_code_str)),
        )
        # 渲染图表
        scatter.render(f"scatter_{name}.html")

    def calc_rtn_by_year(self, df, rule="Y",):
        total = []
        for i, _df in df.resample(rule):
            _s = (1+_df).cumprod()
            if rule == "Y":
                colname = i.year
            else:
                colname = f"{i.year}{i.month:0>2d}"
            s = _s.iloc[-1] - 1  # 每年收益率
            s.name = colname
            total.append(s)
            # total=total.append(pd.DataFrame(s))
        total = pd.DataFrame(total)
        return total

    def calcSharpRatio(self, df):
        # 无风险年化收益率为2%
        # 除非无风险利率波动较大（如在新兴市场中一样），否则超额收益和原始收益的标准差将相似

        r = round(df['return'].mean()/df['return'].std()*np.sqrt(252), 3)
        print("夏普率", r)
        # 减去无风险利率
        df["rtn"] = df["return"] - 0.02/252
        # 由日频率转化为年化夏普
        # https://www.zhihu.com/question/27264526 不同周期选择参考优劣参考
        r = round(df['rtn'].mean()/df['rtn'].std()*np.sqrt(252), 3)
        print("夏普率扣除无风险收益后", r)

    @Decorator.loadData(path="data")
    def qryShiborData(self, **kawgrs):
        if "year" not in kawgrs:
            # 汇总
            total = pd.DataFrame(
                columns=["曲线名称", "日期", "3月", "6月",
                         "1年", "3年", "5年", "7年", "10年", "30年"])
            for year in range(2006, 2023):
                _df = self.qryShiborData(year=year)
                _df['date'] = pd.to_datetime(_df["日期"], format='%Y-%m-%d')
                _df.set_index('date', inplace=True)
                total = total.append(_df)
            return total

        import akshare as ak
        year = kawgrs["year"]
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        bond_china_yield_df = ak.bond_china_yield(
            start_date=start_date, end_date=end_date)
        return bond_china_yield_df

    # def get_minute_data(self, symbol,
    #                     date_time,
    #                     minute=931):
    #     url = "http://192.168.1.100:5000/stock"
    #     params = {}
    #     params["code"] = symbol[:2]+"SE"+symbol[2:]
    #     params["begin"] = date_time
    #     params["end"] = date_time
    #     params["minute"] = minute
    #     rsp = requests.get(url=url, params=params)
    #     data_json = demjson.decode(rsp.text)
    #     print(data_json)

    # @Decorator.firstLoad
    @Decorator.loadData(path="data")
    def get_minutes_data(self, symbol, date_time, **kwargs):
        # 分钟线数据 只保留01到10分的时间戳
        # http://192.168.1.100:5000/stock?code=SHSE.600000&begin=20220104&end=20221231&minute=0931,1400,1430
        # 开高低收
        # 定义交易日起始时间和结束时间
        start_time = pd.Timestamp('09:30:00')
        end_time = pd.Timestamp('15:00:00')
        df = pd.DataFrame(columns=['date_time', "hour_minute", 'open',
                                   'high', 'low', 'close', 'volume'])
        # 定义时间间隔
        interval = pd.Timedelta(minutes=5)

        # 生成时间戳列表
        timestamps = []
        for timestamp in pd.date_range(start=start_time,
                                       end=end_time,
                                       freq=interval):
            timestamps.append(timestamp.time().strftime("%H%M"))

        url = "http://192.168.1.100:5000/stock"
        params = {}
        params["code"] = symbol[:2]+"SE"+symbol[2:]
        params["begin"] = date_time
        params["end"] = date_time
        params["minute"] = ",".join(timestamps)
        rsp = requests.get(url=url, params=params)
        print(demjson.decode(rsp.text))
        data_json = demjson.decode(rsp.text)["info"]
        for date, values in data_json.items():
            for value in values:
                hour_minute = int(value[0])
                open_price = value[1]
                high_price = value[2]
                low_price = value[3]
                close_price = value[4]
                volume = value[5]
                #  只保留日期
                date_time = pd.to_datetime(date, format='%Y-%m-%d').date()
                # hour_minute = pd.to_datetime(hour_minute,
                #                              format='%H%M%S').time()
                df = df.append({'date_time': date_time,
                                'hour_minute': hour_minute,
                                'open': open_price,
                                'high': high_price,
                                'low': low_price,
                                'close': close_price,
                                'volume': volume}, ignore_index=True)
        df.set_index('date_time', inplace=True)
        return df


def test_genReturn():
    mgr = Mgr()
    rate = mgr.genReturn(beg=20240108,
                         end=20240109,
                         symbols=["SZ.000001", "SZ.000002"],
                         weight=[0.5, 0.5])
    print(rate)


if __name__ == '__main__':
    # m = Mgr()
    # m.genSymbolRateData(symbol="SH.600057", is_real_time=True)
    test_genReturn()
