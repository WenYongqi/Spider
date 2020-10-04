import requests
from bs4 import BeautifulSoup
import json
import xlsxwriter

info=[]
Headers={
    'referer':'https://stock.sohu.com/',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

def calc(code,month):
    url='https://q.stock.sohu.com/hisHq?code=cn_'+code+'&start=20200'+str(month)+'01&end=20200'+str(month)+'31'
    html=requests.get(url,headers=Headers).text
    try:
        data=json.loads(html)[0]['hq']
    except KeyError:
        return 0,0
    n=len(data)
    sum=0
    for i in range(0,n-1):
        sum+=round((float(data[i][1])/float(data[i+1][2])-1)*10000)/10000.0
    return n-1,sum/max(1,(n-1))
pos=0
info.append(['代码','名称','现价','溢价率','6月','5月','4,5月','3,4,5月','4月','3月','正股名称','正股代码','正股6月','正股5月','正股4月','正股3月'])
with open('Spider/可转债代码集合.txt','r',encoding='utf-8') as f:
    for line in f:
        row=line[:-1].split(' ')
        june_days,june=calc(row[0],6)
        x,_june=calc(row[5],6)
        may_days,may=calc(row[0],5)
        x,_may=calc(row[5],5)
        april_days,april=calc(row[0],4)
        x,_april=calc(row[5],4)
        march_days,march=calc(row[0],3)
        x,_march=calc(row[5],3)
        try:
            one=round((may*may_days)/(may_days)*10000)/10000.0
        except ZeroDivisionError:
            one='None'
        try:
            two=round((may*may_days+april*april_days)/(may_days+april_days)*10000)/10000.0
        except ZeroDivisionError:
            two='None'
        try:
            three=round((may*may_days+april*april_days+march*march_days)/(may_days+april_days+march_days)*10000)/10000.0
        except ZeroDivisionError:
            three='None'
        info.append([row[0],row[1],row[2],row[3],june,one,two,three,april,march,row[4],row[5],_june,_may,_april,_march])
        pos+=1
        print(str(pos)+' is over!')
f.close()

workbook=xlsxwriter.Workbook('Analysis2.xlsx')
worksheet=workbook.add_worksheet()
for i in range(0,len(info)):
    for j in range(0,16):
        worksheet.write(i,j,info[i][j])
workbook.close()
