from flask import Flask
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

@app.route('/<town>')
def index(town):
    
    # 檢查是否有鄉鎮市區代碼檔
    if not os.path.isfile('district.csv'):
        df = pd.read_excel('https://www.stat.gov.tw/public/Attachment/712693030RPKUP4RX.xlsx', header=3)
        df.drop(columns=['縣市代碼', '村里代碼', '村里名稱', '村里代碼', '村里代碼.1'], axis=1, inplace=True)
        df.drop_duplicates(inplace=True)
        df.to_csv('district.csv', encoding='big5', index=False)

    dftown = pd.read_csv('district.csv', encoding='big5')  #區鄉鎮名稱代碼資料
    print(dftown)
    town = input('請輸入查詢的鄉鎮市區名稱：')  #要查詢的區鄉鎮名稱 
    dfs = dftown[(dftown['縣市名稱']==town[:3]) & (dftown['區鄉鎮名稱']==town[3:])]
    if len(dfs) > 0:  #區鄉鎮名稱存在
        town_no = str(dfs.iloc[0,1])
        #    print(town_no)
        url = 'https://www.cwb.gov.tw/V8/C/W/Town/MOD/3hr/' + town_no + '_3hr_PC.html'  #三日預報網頁
#    url = 'https://www.cwb.gov.tw/V8/C/W/Town' + town_no + 'Town.html'  #三日預報網頁
#    print(url)
        res = requests.get(url)
#    print(res)
    
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
#    print(soup)
    
    # 整理時間日期欄
#    for t in soup.find_all('span', class_='t'):
        for t in soup.find_all('span', class_='t'):   
            t.replaceWith(t.text + ',')
#        print(t.text)
        for d in soup.find_all('span', class_='d'):
            d.replaceWith(d.text)
#        print(d)
    # 整理天氣示意圖欄
        for img in soup.find_all('img'):
            img.replaceWith(img.get('alt'))
    # 整理溫度及體感溫度欄
        for c in soup.find_all('span', class_='tem-C'):
            c.replaceWith(c.text)
        for f in soup.find_all('span', class_='tem-F'):
            f.replaceWith('') 
    # 整理蒲福風級 
        for w1 in soup.find_all('span', class_='wind_1'):
            w1.replaceWith(w1.text + ',')
        for w2 in soup.find_all('span', class_='wind_2'):
            w2.replaceWith('')    
        
    # pandas讀取表格
    
# if not os.path.isfile('district.csv'):
#    df = pd.read_excel('https://www.stat.gov.tw/public/Attachment/712693030RPKUP4RX.xlsx', header=3)
#    print(df)
    
#    df.drop(columns=['縣市代碼', '村里代碼', '村里名稱', '村里代碼', '村里代碼.1'], axis=1, inplace=True)
#    df.drop_duplicates(inplace=True)
#    df.to_csv('district.csv', encoding='big5', index=True)    
#    print(df)
#    print(soup)
#    df = pd.read_html(str(soup))[0]
#    print(soup)
    # 資料轉置
#    df1 = df.T
#    print(df1)
    
    # 刪除不需要的欄
#    df1.drop(columns=[1,3,5,7,9,11], axis=1, inplace=True)
    # 重設索引
#    df1.reset_index(inplace=True)
#    print(df1)
    
    # 將index拆分成時間、日期二欄
#    df1[['時間','日期']] = df1['index'].str.split(',', expand=True)
#    df2 = df1['index'].str.split(',', expand=True)
#    print(df1)
    
    
    # 將10拆分成蒲福風級、風向二欄
#    df1[['蒲福風級','風向']] = df1[10].str.split(',', expand=True)
    
    # 刪除index及10二欄
#    df1.drop(columns=['index', 10], inplace=True)
    
        # 修改欄位名稱
        columns = ['日期','時間','天氣狀況','溫度','體感溫度','降雨機率','相對溼度','蒲福風級','風速(m/s)','風向','舒適度']
        df1 = soup
        df1.columns = columns
        # 欄位重新排序
#    df1 = df1[['日期','時間','天氣狀況','溫度','體感溫度','降雨機率','相對溼度','蒲福風級','風速(m/s)','風向','舒適度']]
        print(df1)
    
        # 轉為json回傳
        return df1.to_json(orient='records', force_ascii=False)
#    print(df1.to_json(orient='records', force_ascii=False))

# else:
#    print('無此鄉鎮市區名稱！')
if __name__ == '__main__':
    app.run()