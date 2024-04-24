# -*- coding: utf-8 -*-
from tradeTools import DataMgr
from tradeTools import indexData
import pandas as pd
from tradeTools import Decorator
from tradeTools import helpers
from common import log
from scipy import stats
import os
class Mgr(DataMgr.Mgr):
    def __init__(self,
                #  因子名称
                 factorName:str):
        super(Mgr,self).__init__()
        self.indexData = indexData.IndexData()
        self.factorName = factorName
        self.logFile = f"trace_{factorName}"
        self.outPath = os.path.dirname(__file__)
        self.symbolInfo = helpers.getSymbolsInfo()
        
    def getFactor(self,symbol,dateTime):

        # 定义因子算法
        close,lastDateTime = self.oldDc.get_nearest_price(stock_id = symbol, datetime=dateTime)
        # assert lastDateTime,f"[{symbol}][{dateTime}] 无历史k线数据"
        if not lastDateTime:
            log.WriteLog(self.logFile,f"[{symbol}][{dateTime}] 无历史k线数据")
            return [None,None]
        totalCapital = self.oldDc.get_capital(stock_id=symbol, datetime=lastDateTime)  
        return [totalCapital*close,lastDateTime]
    
    
    def report(self):
        # 1. TOP 20%组合与 BOTTOM 20%组合的月平均收益率差显著（一般取
            # 0.5%以上）且有效性较高（一般在 60%之上）。
        # 2. TOP 40%组合与 BOTTOM 40%组合的月平均收益率差显著（一般取
            # 0.5%以上）且有效性较高（一般在 60%之上）。
        # 3. 在稳定性分析中，因子排名与下期收益率排名的线性关系显著（至
            # 少在 10%的水平上显著）。
        totalEffectiveness = self.getTotalEffectiveness(factorName=self.factorName)
        totalEffectiveness.reset_index(inplace=True)
        totalEffectiveness.set_index(totalEffectiveness.columns.tolist()[0:2],inplace=True)
        totalEffectiveness.columns = pd.MultiIndex.from_arrays([['月均收益率差','月均收益率差','月均收益率差','月均收益率差',"因子排名与收益率排名相关性","因子排名与收益率排名相关性"],
                    ["一档-五档","有效性","一二档-四五档", "有效性" ,"相关系数", "P 值"]])
        totalEffectiveness = totalEffectiveness.iloc[1:]
        totalEffectiveness = totalEffectiveness.astype(float)
        
        # print(totalEffectiveness[("月均收益率差","有效性")])
        df = totalEffectiveness
        def calcPoint(row):
            point = ""
            # print(row)
            for i in [0,2]: # 收益率和有效性
                if abs(row.iloc[i])>=0.005 and row.iloc[i+1]>=0.6:
                    point+="*"
            if not point:
                return "x"
            if row.iloc[-1] <=0.05:# P值
                point+="+"
            if row.iloc[-1] >0.1:
                point+="-"
            if row.iloc[-2]>0:#相关系数
                point = "[+]"+point
            else:
                point = "[-]"+point
            return point
        df["point"] = df.apply(calcPoint, axis=1)
        filepath = os.path.join(self.outPath,f"{self.factorName}_分析报告.xlsx")
        with pd.ExcelWriter(filepath,engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="分析报告")
            indexConf = {
            "SH.000300":20100101,
            "SH.000905":20100101,
            "SH.000852":20150101,
        }
   
            for indexSymbol,begTime in indexConf.items():
                for _use in ["总体","周期","非周期"]:
                    _df = self.genCumprod(factorName=self.factorName,indexSymbol=indexSymbol,begTime=begTime,use =_use )
                    _df.to_excel(writer, sheet_name=f"累积收益率_{indexSymbol}_{_use}")
    @Decorator.loadData() 
    def getTotalEffectiveness(self,factorName,**kwargs):
        indexConf = {
            "SH.000300":20100101,
            "SH.000905":20100101,
            "SH.000852":20150101,
        }
        ret = []
        for indexSymbol,begTime in indexConf.items():
            for _use in ["总体","周期","非周期"]:
                s = self.analysisEffectiveness(factorName=self.factorName,indexSymbol=indexSymbol,begTime=begTime,use =_use )
                ret.append(s)
        df = pd.DataFrame(ret,index=pd.MultiIndex.from_product([list(indexConf.keys()),
                                                    ["总体","周期","非周期"]]),
                          columns=pd.MultiIndex.from_arrays([['月均收益率差','月均收益率差','月均收益率差','月均收益率差',"因子排名与收益率排名相关性","因子排名与收益率排名相关性"],
                          ["一档-五档","有效性","一二档-四五档", "有效性" ,"相关系数", "P 值"]])
                          
                          )
        return df
    
    def analysisEffectiveness(self,factorName:str,indexSymbol:str,begTime:int,use:str,**kwargs): #分析有效性
        # Step1 将股票池里的样本股票按待测因子按由低到高的顺序分成五档，各占 20%。分别计算每一档的月平均收益率。
        # Step2 计算两次月平均收益率差，分别是：
            # TOP 20%（第一档）- BOTTOM 20%（第五档），
            # TOP 40%（第一、二档）- BOTTOM 40%（第四、五档）。
        # Step3 计算上述收益率差的平均值。如果平均值为正，则该因子的影响总
            # 体是正向的，即因子值越大收益趋于越大；如果平均值为负，则反之。
        # Step4 计算每个因子的有效性。有效性的计算方法如下：
            # 正向(负向)因子的有效性=月均收益率差为正（负）的月份数/总月份数。
        # Step5 根据每个月份五档的因子排名与对应的平均收益率排名，计算其
            # 相关系数以及显著性检验的 P 值。
        df = self.genGroupMonthlyRate(factorName=self.factorName,indexSymbol=indexSymbol,begTime=begTime,use=use)
        df.dropna(inplace =True)
        corrSeries = pd.Series()
        for index,row in df.iterrows():
            rankSerise = pd.Series([int(_index[-1]) for _index in row.index],index=row.index)#排名序列
            corrSeries[index] = rankSerise.corr(row,method="spearman")
        t, p =  stats.ttest_1samp(corrSeries, 0, nan_policy='omit')
       
        df["alpha_T20"] = df["group_1"] - df["group_5"]
        df["alpha_T40"] = df["group_1"]+df["group_2"] - df["group_4"] - df["group_5"]
        df["alpha_T40"] = 0.5*df["alpha_T40"]
        alpha_T20_mean = df["alpha_T20"].mean() # 收益率差
        alpha_T40_mean = df["alpha_T40"].mean() # 收益率差
        eff_T20_cnt =len(df[df["alpha_T20"]>=0]) if alpha_T20_mean>=0 else len(df[df["alpha_T20"]<0])
        eff_T40_cnt =len(df[df["alpha_T40"]>=0]) if alpha_T40_mean>=0 else len(df[df["alpha_T40"]<0])
        effectivenessAlpha_T20 =eff_T20_cnt/len(df["alpha_T20"]) # 有效性
        effectivenessAlpha_T40 = eff_T40_cnt/len(df["alpha_T40"]) # 有效性
        # return pd.Series({
        #     "月均收益率差":{
        #         "alpha_T20_mean":alpha_T20_mean,
        #         "effectivenessAlpha_T20":effectivenessAlpha_T20,
        #         "alpha_T20_mean":alpha_T20_mean,
        #         "effectivenessAlpha_T40":effectivenessAlpha_T40,             
        #                             },
        #     "因子排名与收益率排名相关性":
        #     {
        #         "相关系数":corrSeries.mean(),
        #         "P值":p,
                
        #     }
        #     })
        return [alpha_T20_mean,effectivenessAlpha_T20,alpha_T40_mean,effectivenessAlpha_T40,corrSeries.mean(),p]
    @Decorator.loadData() 
    def genCumprod(self,factorName:str,indexSymbol:str,begTime:int,use:str = "",**kwargs):
        df = self.genGroupMonthlyRate(factorName=self.factorName,indexSymbol=indexSymbol,begTime=begTime,use = use)
        endTime = df.iloc[-1].name # 策略结束时间
        indexDf = self.genIDXData(indexSymbol = indexSymbol)
        indexDf = indexDf[(indexDf.index >= str(begTime))&(indexDf.index <= endTime)]
        indexDf = indexDf[[indexSymbol]].resample('M').apply(lambda x : ((1+x).prod()-1)) # 指数月收益率率
        total = pd.concat([df,indexDf[[indexSymbol]]], axis=1, join='outer', )
        # total["alpha_T20"] = 
        total.dropna(inplace=True)
        total = (1+total).cumprod()
        return total
        
    @Decorator.loadData() 
    def genGroupMonthlyRate(self,factorName:str,indexSymbol:str,begTime:int,use,**kwargs):
        tradeDays = self.genTradeDays(begTime = begTime,frequency=1)
        lastMonthEnd = 0
        monthlyRate = {}
        for monthEnd,row in tradeDays.resample(rule = "M",).last().iterrows():
            print(monthEnd)
            if not lastMonthEnd:
                lastMonthEnd = monthEnd
                continue
            ilastMonthEnd=int(lastMonthEnd.strftime('%Y%m%d'))
            lastMonthEnd = monthEnd
            symbols = self.indexData.getSymbols(dateTime= ilastMonthEnd,indexSymbol = indexSymbol)
            
            if use in ["周期","非周期"]: # 按周期，非周期分类
                symbolinfo = self.symbolInfo[self.symbolInfo['industry'].str.contains('金融|金属|运输|采|房地产')] if use == "周期" else self.symbolInfo[~self.symbolInfo['industry'].str.contains('金融|金属|运输|采|房地产')] 
                symbols = list(set(symbols) & set(symbolinfo.index.tolist()))
            total = []
            for symbol in symbols:
                [x,lastDateTime] = self.getFactor(symbol,ilastMonthEnd)
                total.append(
                    pd.Series(
                        {
                            self.factorName:x,
                            "dateTime":lastDateTime,
                        },
                        name = symbol
                    )
                )
            # return
            df = pd.DataFrame(total)
            df["qcut"] = pd.qcut(df[self.factorName],q=5,labels=[i+1 for i in range(5)])
            
            
            openSymbols = {f"group_{i+1}":df[df.qcut ==i+1].index.tolist() for i in range(5) }
            for groupName,_openSymbols in openSymbols.items():
                seriseMonthRate = []
                for symbol in _openSymbols:
                    _sMonthRate = self.genMonthlyRate(symbol=symbol)
                    # assert monthEnd in _sMonthRate.index,f"{symbol} {monthEnd} 无数据"
                    if monthEnd not in _sMonthRate.index:
                        # 可能的原因是合并或者退市。但是上个月在成分股池中
                        log.WriteLog(self.logFile,f"{symbol} {monthEnd} 无数据")
                        continue
                        
                    s = _sMonthRate.loc[monthEnd]
                    seriseMonthRate.append(s)
                monthDf = pd.DataFrame(seriseMonthRate)
                meanRate = monthDf.rate.mean()
                if groupName not in monthlyRate:
                        monthlyRate[groupName] = {}
                monthlyRate[groupName][monthEnd] = meanRate
        monthlyRate = pd.DataFrame(monthlyRate)
        return monthlyRate

@Decorator.loadData() 
def genIterateArgs(factorName,mgrClass,**kwargs):#参数遍历
    total =[]
    for last in range(3,60,3):
        m = mgrClass(factorName=f"{factorName}_{last}")
        df = m.getTotalEffectiveness(factorName=m.factorName)
        df = df.iloc[:,0:2]
        df["last"] = last
        total.append(df)
    total = pd.concat(total)
    total = total.reset_index()
    total = total.iloc[1:]
    total.columns = ["indexSymbol","type_","alpha","last"]
    return total

def render(factorName,
           df):
    import pyecharts.options as opts
    from pyecharts.charts import Line
    x = [str(last) for last in range(3,60,3)]
    line=(
    Line()
    .add_xaxis(xaxis_data=x)
    )
    
    for indexSymbol in ["SH.000300","SH.000905","SH.000852"]:
        for type_ in ["总体","周期","非周期"]:
        # for type_ in ["总体"]:
            _df=df[(df.indexSymbol ==indexSymbol) & (df.type_ == type_)]
            _df = _df.sort_values(["last"],ascending=True)
            line.add_yaxis(series_name=f"{indexSymbol}_{type_}",
                       y_axis=_df["alpha"].tolist(),
                       label_opts=opts.LabelOpts(is_show=False),
                       )
        
    line.render(f"{factorName}参数遍历.html")
    
if __name__ == '__main__':
    m = Mgr(factorName = "市值因子")
    df = m.report()   

