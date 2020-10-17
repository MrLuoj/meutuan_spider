#coding:utf-8

from requests_html import HTMLSession
import pandas as pd
import os
import pymysql

session = HTMLSession()
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
    "Host": "i.meituan.com",
    "Referer": "https://www.meituan.com/"
}

conn = pymysql.connect("localhost", "root", "", "SHIYI")
cursor = conn.cursor()

df = pd.read_csv('new_data.csv')


def get_info(index):
    index_new = str(index)
    url = 'https://www.meituan.com/xiuxianyule/'
    new_url = os.path.join(url, index)
    # print(new_url)
    print("=======================i================", i)
    print("=======================meituanid================", index_new)
    r = session.get(new_url, headers=header)

    sel_name = '#lego-widget-play-mt-poi-001-000 > div > div.poi-detail.clearfix > div.seller-info-head > h1'
    results_name = r.html.find(sel_name)

    sel_address = '#lego-widget-play-mt-poi-001-000 > div > div.poi-detail.clearfix > div.seller-info-head > div.seller-info-body > div:nth-child(1) > a > span'
    results_address = r.html.find(sel_address)

    sel_time = '#lego-widget-play-mt-poi-001-000 > div > div.poi-detail.clearfix > div.seller-info-head > div.seller-info-body > div:nth-child(3) > span:nth-child(2)'
    results_time = r.html.find(sel_time)

    sel_consume = '#lego-widget-play-mt-poi-001-000 > div > div.poi-detail.clearfix > div.seller-info-head > div.row > span'
    results_consume = r.html.find(sel_consume)

    sel_consume_score = '#lego-widget-play-mt-poi-001-000 > div > div.poi-detail.clearfix > div.seller-info-head > div.row > span > span'
    results_consume_score = r.html.find(sel_consume_score)

    sel_phone = '#lego-widget-play-mt-poi-001-000 > div > div.poi-detail.clearfix > div.seller-info-head > div.seller-info-body > div:nth-child(2) > span:nth-child(2)'
    results_phone = r.html.find(sel_phone)

    #     print(results_name[0].text)
    #     print(results_address[0].text)
    #     print(results_time[0].text)
    #     print(results_consume[0].text[0:3])
    #     print(results_consume[0].text[8:10])

    if results_name == []:
        print("None")
    else:
        print(results_name[0].text)

    if results_address == []:
        print("None")
    else:
        print(results_address[0].text)

    if results_time == []:
        print("None")
    else:
        print(results_time[0].text)

    if results_phone == []:
        print("None")
    else:
        print(results_phone[0].text)

    if results_consume == []:
        print("None")
    else:
        print(results_consume[0].text[0:3].strip('分'))
        # print(results_consume[0].text[8:10])
        print(results_consume_score[0].text)
    if results_name != [] and results_address != [] and results_time != [] and results_phone != [] and results_consume != []:
        sql = "insert into mt_test5(meituanid,companyname,companyaddress,businesstime,destinephone,score,averagecost)" \
              "values('%s','%s','%s','%s','%s','%s','%s')" \
              % (index_new, results_name[0].text, results_address[0].text, results_time[0].text, results_phone[0].text,
                 results_consume[0].text[0:3].strip('分'), results_consume_score[0].text)
        cursor.execute(sql)
        conn.commit()

    if results_name == [] and results_address != [] and results_time != [] and results_phone != [] and results_consume != []:
        sql = "insert into mt_test5(meituanid,companyname,companyaddress,businesstime,destinephone,score,averagecost)" \
              "values('%s','%s','%s','%s','%s','%s','%s')" \
              % (index_new, '', results_address[0].text, results_time[0].text, results_phone[0].text,
                 results_consume[0].text[0:3].strip('分'), results_consume_score[0].text)
        cursor.execute(sql)
        conn.commit()

    if results_name != [] and results_address == [] and results_time != [] and results_phone != [] and results_consume != []:
        sql = "insert into mt_test5(meituanid,companyname,companyaddress,businesstime,destinephone,score,averagecost)" \
              "values('%s','%s','%s','%s','%s','%s','%s')" \
              % (index_new, results_name[0].text, '', results_time[0].text, results_phone[0].text,
                 results_consume[0].text[0:3].strip('分'), results_consume_score[0].text)
        cursor.execute(sql)
        conn.commit()

    if results_name != [] and results_address != [] and results_time == [] and results_phone != [] and results_consume != []:
        sql = "insert into mt_test5(meituanid,companyname,companyaddress,businesstime,destinephone,score,averagecost)" \
              "values('%s','%s','%s','%s','%s','%s','%s')" \
              % (index_new, results_name[0].text, results_address[0].text, '', results_phone[0].text,
                 results_consume[0].text[0:3].strip('分'), results_consume_score[0].text)
        cursor.execute(sql)
        conn.commit()

    if results_name != [] and results_address != [] and results_time != [] and results_phone == [] and results_consume != []:
        sql = "insert into mt_test5(meituanid,companyname,companyaddress,businesstime,destinephone,score,averagecost)" \
              "values('%s','%s','%s','%s','%s','%s','%s')" \
              % (index_new, results_name[0].text, results_address[0].text, results_time[0].text, '',
                 results_consume[0].text[0:3].strip('分'), results_consume_score[0].text)
        cursor.execute(sql)
        conn.commit()

for i in range(0, 100):
    print(i)
    if df['meituanid'][i] != None:
        get_info(df['meituanid'][i])

