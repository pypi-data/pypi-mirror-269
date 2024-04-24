# -*- coding: utf-8 -*-
# @Time    : 2018/8/10 14:01
# @Author  : hc
# @Site    :
# @File    : Decorator.py
# @Software: PyCharm
from functools import wraps
import os
import pandas as pd
from common import basefunc
import inspect
from enum import Enum


def singleton(cls, *args, **kwargs):
    instance = {}  # 创建字典来保存实例

    def get_instance(*args, **kwargs):
        if cls not in instance:  # 若实例不存在则新建
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return get_instance


# 装饰器 对实例方法的首次加载
def firstLoad(func):  # 装饰器不带函数的写法
    @wraps(func)
    def inner_wrapper(*args, **kwargs):  # 被装饰的函数的参数
        # print (args,kwargs)
        _obj = args[0]  # 实例对象
        attrname = func.__name__[3:]
        if not hasattr(_obj, attrname):
            setattr(_obj, attrname, {})
        symbol = kwargs["symbol"] if "symbol" in kwargs else kwargs["index_symbol"]
        if symbol not in getattr(_obj, attrname):
            getattr(_obj, attrname)[symbol] = func(*args, **kwargs)
        return getattr(_obj, attrname)[symbol]
    return inner_wrapper


# 装饰器，优先加载静态文件
def loadData(*dargs, **dkargs):
    def outer(func, *args, **kwargs):
        sig = inspect.signature(func)
        # 获取函数被调用的堆栈信息
        # stack = inspect.stack()
        @wraps(func)
        def inner(*args, **kwargs):
            # 获取方法所有参数（包括默认参数）
            arguments = {}
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            for key, value in bound.arguments.items():
                if key == "kwargs":
                    for _k, _v in bound.arguments[key].items():
                        arguments[_k] = _v
                else:
                    arguments[key] = value
            excelNames = []
            # 过滤以下参数不作为文件名标识
            _filter_arguments = ["is_real_time",
                                 "parse_dates",
                                 "is_to_csv",
                                 "fileName"]
            for k, v in arguments.items():  # 参数的键值对作为补充文件名
                if k in _filter_arguments:
                    continue
                if not isinstance(v, (str, int, bool, Enum)):
                    continue
                excelNames.append(k)
            excelNames.sort()
            # 构造excel文件名
            # eg. 方法名_参数名[参数值]... .csv
            # get_factor_after_standard ->_factor_after_standard
            func_name = func.__name__[3:]
            excelName = f"{func_name}"
            for k in excelNames:
                if isinstance(arguments[k], Enum):
                    excelName += f"_{k}[{arguments[k].name}]"
                    continue
                excelName += f"_{k}[{str(arguments[k])}]"
            excelName += ".csv"
            co_filename = os.path.normcase(func.__code__.co_filename)
            # co_filename = stack[1].filename
            # 定位到工作空间目录 workspace
            workspace = basefunc.get_path_dirname()
            _paths = workspace.split("\\")
            _paths.append("data")

            if "path" in dkargs and dkargs["path"] == "data":
                # 装饰器传参 path：设置为"data".则读取data路径。用于可复用的数据
                dataPath = ""
            else:
                # 取函数所在的代码文件名 _ 分割的第1个关键字 作为文件夹名
                dataPath = co_filename.split(
                    "\\")[-1].split(".")[0].split("_")[0]
                dataPath = "_".join([dataPath])
                _paths.append(dataPath)
            _paths.append(func_name)
            _paths.append(excelName)
            _fileName = arguments.get('fileName', False)
            if not _fileName:
                _fileName = os.sep.join(_paths)  #
            path = os.path.dirname(_fileName)
            if not os.path.exists(path):
                os.makedirs(path)

            is_real_time = arguments.get('is_real_time', False)
            parse_dates = arguments.get('parse_dates', -1)
            # is_to_csv false:只执行方法不写入静态文件。
            # 子类调用父类时会用到.避免覆盖父类的静态数据文件
            is_to_csv = arguments.get('is_to_csv', True)
            if not os.path.exists(_fileName) or is_real_time:
                # 传入fileName,用于是否保留原有数据，在函数内自行处理
                if "fileName" not in kwargs:
                    df = func(fileName=_fileName, *args, **kwargs)
                else:
                    # fileName已经在kwargs中
                    df = func(*args, **kwargs)
                if is_to_csv:
                    print(func.__name__ + f"\033[32m生成数据[{_fileName}]\033[0m")
                    df.to_csv(_fileName, encoding="UTF-8")

            if is_to_csv:
                print(func.__name__ + f"读取数据[{_fileName}]")
                if parse_dates == -1:
                    # 注意解析csv异常 第一列作为索引
                    df = pd.read_csv(_fileName, index_col=0)
                else:
                    df = pd.read_csv(_fileName,
                                     index_col=0,
                                     # parse_dates尝试指定转化时间格式的列
                                     parse_dates=parse_dates)
            try:
                df.index = pd.to_datetime(df.index, format='mixed')
            except Exception as e:
                # print(e)
                pass
            return df
        return inner
    return outer
