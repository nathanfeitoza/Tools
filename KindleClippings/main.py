#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 21:50:19 2019

@author: Lucifer
@site: plantree.me
@contact: wpy1174555847@outlook.com
"""
from bs4 import BeautifulSoup
import math
import pandas as pd

# 日期格式转换
def transform_date(date):
    for i in ['年', '月', '日', '星期', '一', '二', '三', '四', '五', '六', '天', '日', '上午', '下午']:
        date = date.replace(i, ' ')
    return date 


with open('My Clippings.txt', encoding='utf-8-sig') as f:
    lines = f.readlines()

time_series = pd.Series()
books = {}

# 记录数目
num = math.ceil(len(lines) / 5)

for i in range(num):
    item = lines[i*5: (i+1)*5]
    title = item[0].strip().replace('\ufeff', '')
    content = item[-2].strip()
    date = item[1].split(' ')
    date = date[-2] + date[-1].strip()
    if title in books.keys():
        books[title].append([date, content])
    else:
        books[title] = []
    series = pd.Series([transform_date(date)])
    # 日期记录
    time_series = time_series.append(series)
    
time_series = pd.to_datetime(time_series)
time_series = time_series.sort_values()
start_time = time_series.iloc[0, ]
end_time = time_series.iloc[num-1, ]
time_delta = end_time - start_time
days = time_delta.days

# reander
with open('index.html') as f:
    bsObj = BeautifulSoup(f.read(), 'lxml')

# add abstract
day = bsObj.find('span', attrs={'class': 'day'})
day.string = str(days)
book = bsObj.find('span', attrs={'class': 'book'})
book.string = str(len(books))
highlight = bsObj.find('span', attrs={'class': 'highlight'})
highlight.string = str(num)

# add books
container = bsObj.find('div', attrs={'class': 'books'})
for name in books.keys():
    details = bsObj.new_tag('details')
    summary = bsObj.new_tag('summary')
    summary.string = name
    ol = bsObj.new_tag('ol')
    for item in books[name]:
        li = bsObj.new_tag('li')
        li.string = item[1] + 10 * '-' + item[0]
        ol.append(li)
    details.append(summary)
    details.append(ol)
    container.append(details)

with open('result.html', 'w') as f:
    f.write(str(bsObj))
    print('create successfully')

    
    
    
    
    
    
    
    
    
    
    
    
    










