import requests
from bs4 import BeautifulSoup


# トークンID
token="TOKEN"


# LINE Notify APIのURL
url="https://notify-api.line.me/api/notify"


# WEBスクレイピング対象のURL
tenki_url="https://weather.yahoo.co.jp/weather/jp/13/4410.html"
response=requests.get(tenki_url)


# WEBスクレイピング対象のHTML
html=BeautifulSoup(response.text,"html.parser")


# 今日の天気に関するすべての情報を抽出
forecast=html.find_all("div",attrs={"class":"forecastCity"})[0]
today=forecast.find_all("div")[0]

# 今日の天気のみを取得
weather=today.find_all("p",attrs={"class":"pict"})[0].text.replace("\n","").replace(" ","")


# 今日の最高気温を取得
high=today.find_all("li")[0].text


# 今日の最低気温を取得
low=today.find_all("li")[1].text


# 時間帯毎の降水確率を取得
rain_06=today.find_all("td")[4].text
rain_0612=today.find_all("td")[5].text
rain_1218=today.find_all("td")[6].text
rain_1824=today.find_all("td")[7].text


# 天気、気温、降水確率の情報を変数に格納
message="""
本日の天気 {}
最高気温 {}
最低気温 {}
降水確率 
0-6時：{}
12-18時：{}
18-24時：{}
""".format(weather,high,low,rain_06,rain_0612,rain_1218,rain_1824)

# LINE Notify APIを実行
auth={"Authorization":"Bearer "+token}
content={"message":message}
requests.post(url,headers=auth,data=content)