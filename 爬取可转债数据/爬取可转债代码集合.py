import requests
from bs4 import BeautifulSoup
import os
import re
import json

Headers={
    'referer':'https://www.jisilu.cn/',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}
url='https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t=1591497295176'

r=requests.get(url,headers=Headers)
html=r.text
info=json.loads(html)

with open('可转债代码集合.txt','w',encoding='utf-8') as f:
    for i in range(0,282):
        if info['rows'][i]['cell']['price_tips'] != '待上市':
            f.write(info['rows'][i]['id']+' '+info['rows'][i]['cell']['bond_nm']+' '+info['rows'][i]['cell']['price']+' '+info['rows'][i]['cell']['premium_rt']+' '+info['rows'][i]['cell']['stock_nm']+' '+info['rows'][i]['cell']['stock_cd']+' '+info['rows'][i]['cell']['curr_iss_amt']+'\n')
