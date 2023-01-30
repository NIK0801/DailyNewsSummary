import feedparser
import csv
import pandas as pd
import re
import time
from email.utils import parsedate
from config import our_feeds, f_all_news, f_certain_news
import datetime
from datetime import datetime as DT, timedelta
import pytz
#from datetime import datetime, timedelta
def check_url(url_feed):
    lenta = feedparser.parse(url_feed)
    return lenta

def take_data():
    d = {}
    d1 = {}
    data = []
    tz1 = pytz.timezone('Europe/Moscow')
    tz2 = pytz.timezone('UTC')
    for key, url in our_feeds.items():        
        lenta = check_url(url)
        for item_of_news in lenta['items']:
            d['title'] = item_of_news['title']
            d['description'] = re.sub(r"<[^>]+>", "", item_of_news['description'], flags=re.S)
            d['description'] = re.sub(" +", " ", d['description'])
            d['link'] = item_of_news['link']
            d['date'] = item_of_news['published']           
            try:
                d['category'] = item_of_news['category']
            except:
                d['category'] = 'не указана'
            
            date_unf = parsedate(d['date'])
            date = time.strftime("%d-%m-%Y", date_unf)
            date_to_write = time.strftime("%d-%m-%Y %H:%M", date_unf)
            dt_tz2 = tz1.localize(DT.strptime(date_to_write, "%d-%m-%Y %H:%M")).astimezone(tz2).strftime("%d-%m-%Y %H:%M")
            d['date']  = date_to_write
            now = datetime.datetime.now()  
            #now = now.strftime("%d-%m-%Y")
            
            result_date = now - timedelta(days=1)
            result_date = time.strftime("%d-%m-%Y %H:%M", result_date.timetuple())
            
            if dt_tz2 >= result_date:                
                d1 = d
                d = {}
                data.append(d1)            
    return data
        
def write_all_news():
    news = take_data()
    header = ['Заголовок', 'Контент', 'Ссылка', 'Дата публикации', 'Категория']
    with open(f_all_news, 'w', encoding = 'utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(i for i in header)
        for new in news:
            writer.writerow((new['title'],new['description'],new['link']+"\t",new['date'],new['category']))
    
def looking_for_certain_news(target1, target2):
    write_all_news()
    now = datetime.datetime.now()
    date = str(now.strftime("%d-%m-%Y"))
    df = pd.read_csv(f_all_news)
    result = df.apply(lambda x: x.str.contains(target1, na=False, flags = re.IGNORECASE, regex = True)).any(axis = 1)
    result2 = df.apply(lambda x: x.str.contains(target2, na=False, flags = re.IGNORECASE, regex = True)).any(axis = 1)
    new_df = df[result&result2]
    new_df.to_csv(f_certain_news, encoding = 'utf-8-sig')
    #new_df.drop(new_df.columns[[0]], axis = 1)
    df = pd.read_csv(f_certain_news)
    df.to_excel('db/NewsMediaParse'+date+'.xlsx', index=False)#.drop(new_df.columns[0], axis = 1)