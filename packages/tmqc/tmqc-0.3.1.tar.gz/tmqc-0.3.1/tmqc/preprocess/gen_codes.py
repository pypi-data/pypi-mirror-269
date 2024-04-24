import os
import re
import traceback
from datetime import datetime, timedelta

from common import log
from tradeTools import helpers


def load_codes(root):
    reQuery = True
    stock_info = []
    today_date = datetime.now()

    codeFile =os.path.join(root, 'rec/codes.txt')
    if not os.path.exists(codeFile):
        log.WriteLog("sys", f"codeFile not exists {codeFile}")
    else:
        log.WriteLog("sys", f"codeFile exists {codeFile}")
        try:
            with open(codeFile,'rt', encoding='utf8') as f:
                c = f.read()
                if len(c) >0:
                    ls = c.split('\n')
                    date_from_ls = datetime.strptime(ls[0], '%Y%m%d')
                    if (today_date - date_from_ls) < timedelta(days=10):
                        reQuery = False
                    for line in ls[1:]:
                        try:
                            e = re.split(r'\s+', line)
                            stock_info.append({'code': e[0], 'name': e[1]})
                        except Exception:
                            pass
        except Exception as e:
            log.WriteLog("sys", str(traceback.format_exc()))

    log.WriteLog("sys", "codes loaded %s" % len(stock_info))

    if reQuery:
        log.WriteLog("sys", "query codes from web......")
        codes = helpers.get_codes_from_web()
        if len(codes):
            stock_info = codes
            with open(codeFile, 'w', encoding='utf-8') as f:
                today_date_ls = today_date.strftime('%Y%m%d')
                f.write(f'{today_date_ls}\n')
                for info in stock_info:
                    f.write(f'{info["code"]}\t{info["name"]}\n')

    return reQuery, stock_info


if __name__ == '__main__':
    reQuery, stock_info = load_codes('')
    print('Query new:', 'yes' if reQuery else 'no')

    print('print 10 codes')
    for si in stock_info[:10]:
        print(si)

