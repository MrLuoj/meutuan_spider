#coding:utf-8

import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymysql

conn = pymysql.connect("localhost", "root", "lj910729", "SHIYI")
cursor = conn.cursor()

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
    "Host": "i.meituan.com",
    "Referer": "https://www.meituan.com/"
}

url = "https://www.meituan.com/xiuxianyule/"
csv_file_path = './kdw_comp_manual_relation_info.csv'

def getHtmlText(url):
    try:
        r = requests.get(url, timeout = 30,headers = headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except :
        return ""

def getUrlList(path,url):
    df = pd.read_csv(path)
    UrlList = []
    for id in df['meituanid']:
        trueurl = url + str(id)
        UrlList.append(trueurl)
    return UrlList


def getdata(url):
    html = getHtmlText(url)
    soup = BeautifulSoup(html, 'lxml')
    try:
        all_info = soup.find(attrs={'class': 'seller-info-head'})
        name = all_info.find(attrs={'class': 'seller-name'}).string.strip()
        detail = all_info.find_all('div', attrs={'class': 'item'})
        score_and_consume = all_info.find_all('span', attrs={'class': 'score'})

        score_and_consume = [span.get_text().strip().split() for span in score_and_consume]
        score = score_and_consume[0][0].strip("分")
        consume = score_and_consume[0][1].strip("人均")

        info = []
        info.append(name)
        info.append(score)
        info.append(consume)

        for child in detail:
            detail_info = ''.join(child.find_all('span')[1].string.splitlines())
            info.append(detail_info)
        return info
    except:
        print("没有这页面")
        return None


if __name__ == "__main__":

    Url = getUrlList(csv_file_path,url)
    total_data = []
    for url_addr in Url:
        detail_data = getdata(url_addr)
        total_data.append(detail_data)
        if detail_data == None:
            detail_data = [None] *6  #没有数据的填充none
        else:
            detail_data += [None for i in range(6 - len(detail_data))] #保证每个列表长度是4
        print(detail_data)
        sql = "insert into meituan_new2(companyname,score,averageconsume,companyaddress,destinephone,businesstime)" \
                  "values('%s','%s','%s','%s','%s','%s')" \
                  % (detail_data[0], detail_data[1],detail_data[2], detail_data[3],detail_data[4], detail_data[5])
        cursor.execute(sql)
        conn.commit()