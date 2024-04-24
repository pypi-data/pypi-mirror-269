class CodeFunc:
    # 上海证券交易所的股票代码前缀
    SH_STOCK_PREFIX = ('600', '601', '603', '605', '688', '689')  # A股主板和科创板
    SH_FUND_PREFIX = ('50', '51', '58', '56')  # 基金
    SH_B_SHARES_PREFIX = ('90',)  # B股
    SH_CONVERTIBLE_BOND_PREFIX = ('110', '113')  # 可转债
    SH_REPURCHASE_PREFIX = ('204',)  # 国债回购

    # 深圳证券交易所的股票代码前缀
    SZ_STOCK_PREFIX = ('000', '001', '002', '003', '300', '301')  # A股主板和创业板
    SZ_FUND_PREFIX = ('15',)  # 基金

    SZ_B_SHARES_PREFIX = ('200',)  # B股
    SZ_CONVERTIBLE_BOND_PREFIX = ('12',)  # 可转债
    SZ_REPURCHASE_PREFIX = ('131',)  # 国债回购

    # 北京证券交易所A股
    BJ_STOCK_PREFIX = ('4', '8')

    @staticmethod
    def add_prefix(code):
        """给没有前缀的股票代码增加前缀"""
        if isinstance(code, int):
            if code < 999999:
                code = '%06d' % (code)
            else:
                code = '%s' % (code)
        code = code.upper()

        # 'sh333333'/'sh.333333' -> 'SH.333333'
        if code.startswith(('SH', 'SZ')):
            if code[2] != '.':
                return code[:2] + '.' + code[2:]
            return code

        # '333333sh'/'333333.sh' -> 'SH.333333'
        if code.endswith(('SH', 'SZ')):
            if code[-3] != '.':
                return code[-2:] + '.' + code[:-2]
            return code[-2:] + '.' + code[:-3]

        ex = CodeFunc.get_stock_exchange(code)
        return f'{ex}.{code}'

    @staticmethod
    def get_stock_exchange(stock_code):
        """判断股票ID对应的证券市场
        :param stock_code: 股票ID, 若以 'SZ', 'SH'开头直接返回对应类型，否则使用内置规则判断
        :return: 'SH' or 'SZ'
        """
        if isinstance(stock_code, int) and stock_code < 999999:
            stock_code = '%06d' % (stock_code)

        if len(stock_code) == 8:  # 期权
            if stock_code.startswith('10'):
                return 'SH'
            if stock_code.startswith('90'):
                return 'SZ'
        else:
            stock_code = stock_code[-6:]
            if stock_code.startswith(CodeFunc.SH_STOCK_PREFIX
                                    + CodeFunc.SH_FUND_PREFIX
                                    + CodeFunc.SH_B_SHARES_PREFIX
                                    + CodeFunc.SH_CONVERTIBLE_BOND_PREFIX
                                    + CodeFunc.SH_REPURCHASE_PREFIX):
                return 'SH'
            if stock_code.startswith(CodeFunc.SZ_STOCK_PREFIX
                                    + CodeFunc.SZ_FUND_PREFIX
                                    + CodeFunc.SZ_B_SHARES_PREFIX
                                    + CodeFunc.SZ_CONVERTIBLE_BOND_PREFIX
                                    + CodeFunc.SZ_REPURCHASE_PREFIX):
                return 'SZ'
            if stock_code.startswith(CodeFunc.BJ_STOCK_PREFIX):
                return 'BJ'

    @staticmethod
    def get_stock_type(code):
        """
        判断代码是属于那种类型，目前支持 ['stock', 'fund', 'b_shares', 'convertible_bond', 'repurchase']
        :return: str 返回code类型, stock 股票, fund 基金, b_shares B股, convertible_bond 可转债, repurchase 国债回购
        """
        if code.startswith(CodeFunc.SH_STOCK_PREFIX + CodeFunc.SZ_STOCK_PREFIX):
            return 'stock'
        if code.startswith(CodeFunc.SH_FUND_PREFIX):
            return 'fund'
        if code.startswith(CodeFunc.SH_B_SHARES_PREFIX + CodeFunc.SZ_B_SHARES_PREFIX):
            return 'b_shares'
        if code.startswith(CodeFunc.SH_CONVERTIBLE_BOND_PREFIX + CodeFunc.SZ_CONVERTIBLE_BOND_PREFIX):
            return 'convertible_bond'
        if code.startswith(CodeFunc.SH_REPURCHASE_PREFIX + CodeFunc.SZ_REPURCHASE_PREFIX):
            return 'repurchase'
        return None
