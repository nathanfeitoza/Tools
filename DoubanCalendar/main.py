#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 18:56:52 2019

@author: Eric
@site: plantree.me
@contact: wpy1174555847@outlook.com
"""

from bs4 import BeautifulSoup
import requests
import json
import sxtwl
import random
import math

def parse_movies():
    pages = [25 * i for i in range(10)]
    results = []
    count = 0
    
    for page in pages:
        url = 'https://movie.douban.com/top250?start={0}&filter='.format(page)
        res = requests.get(url).text
        bsObj = BeautifulSoup(res, 'lxml')
        movies = bsObj.find('ol', attrs={'class': 'grid_view'}).find_all('li')
        
        for movie in movies:
            count += 1
            item = {}
            image = movie.find('img')['src']
            title = movie.find('span', attrs={'class': 'title'}).text
            info = movie.find('p', attrs={'class': ''}).text.strip()
            star = movie.find('span', attrs={'class': 'rating_num'}).text
            comment = movie.find('span', attrs={'class': 'inq'})
            if comment is None:
                comment = ''
            else:
                comment = comment.text
            item['image'] = image
            item['title'] = title
            item['info'] = info
            item['star'] = star
            item['comment'] = comment
            results.append(item)
    with open('movies.json', 'w') as f:
        f.write(json.dumps(results))
    print('parse movies successfully')

def parse_books():
    pages = [25 * i for i in range(10)]
    results = []
    count = 0
    
    for page in pages:
        url = 'https://book.douban.com/top250?start={0}&filter='.format(page)
        res = requests.get(url).text
        bsObj = BeautifulSoup(res, 'lxml')
        books = bsObj.find('div', attrs={'class': 'article'}).find_all('table')
        
        for book in books:
            item = {}
            image = book.find('img')['src']
            title = book.find('div', attrs={'class': 'pl2'}).find('a').text.strip()
            info = book.find('p', attrs={'class': 'pl'}).text
            star = book.find('span', attrs={'class': 'rating_nums'}).text
            comment = book.find('span', attrs={'class': 'inq'})
            if comment is None:
                comment = ''
            else:
                comment = comment.text
            item['image'] = image
            item['title'] = title
            item['info'] = info
            item['star'] = star
            item['comment'] = comment
            results.append(item)
    with open('books.json', 'w') as f:
        f.write(json.dumps(results))
    print('parse books successfully')

def get_day(day):
    Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    ShX = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    numCn = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    Week = ["日", "一", "二", "三", "四", "五", "六"]
    jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑","白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"]
    ymc = ["十一", "十二", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十" ]
    rmc = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]
    info = {}
    info['month'] = day.m
    info['day'] = day.d
    info['week'] = Week[day.week]
    year = sxtwl.Lunar().getYearCal(day.Lyear0 + 1984)
    info['n_year'] = Gan[year.yearGan] + Zhi[year.yearZhi]
    info['n_month'] = ymc[day.Lmc]
    info['n_day'] = rmc[day.Ldi]
    if (day.qk >= 0):
        info['jq'] = jqmc[day.jqmc]
    else:
        info['jq'] = ''
    return info

def parse_dates():
    lunar = sxtwl.Lunar()
    res = []
    for i in range(1, 13):
        month = lunar.yueLiCalc(2019, i)
        days = month.days
        for day in days:
            res.append(get_day(day))
    with open('dates.json', 'w') as f:
        f.write(json.dumps(res))
    print('parse dates successfully')


def create_html(start=0, end=365):
    with open('movie_book.json', 'r') as f:
        movie_books = json.loads(f.read())
    with open('dates.json', 'r') as f:
        dates = json.loads(f.read())
    with open('index.html', 'r') as f:
        bsObj = BeautifulSoup(f.read(), 'lxml')

    root = bsObj.find('div', attrs={'id': 'douban'})
    page = math.ceil((end - start) / 4)

    for i in range(0, page):
        i = start + i
        for j in range(4):
            j = i + j * page
            if j < end:
                movie_book = movie_books[j]
                date = dates[j]
                container0 = bsObj.new_tag('div')
                img = bsObj.new_tag('img', src=movie_book['image'])

                container1 = bsObj.new_tag('div')
                container1['class'] = 'info'
                p1 = bsObj.new_tag('p')
                p1.string = movie_book['title']
                p2 = bsObj.new_tag('p')
                p2.string = '豆瓣评分: '
                span = bsObj.new_tag('span')
                span['class'] = 'star'
                span.string = movie_book['star']
                p2.append(span)
                p3 = bsObj.new_tag('p')
                p3.string = movie_book['info']
                p4 = bsObj.new_tag('p')
                container1.append(p1)
                container1.append(p2)
                container1.append(p3)

                container2 = bsObj.new_tag('div')
                container2['class'] = 'comment'
                p5 = bsObj.new_tag('p')
                if movie_book['comment'] != '':
                    p5.string = '“' + movie_book['comment'] + '”'
                else:
                    p5.string = ''
                container2.append(p5)

                container3 = bsObj.new_tag('div')
                container3['class'] = 'date'
                p6 = bsObj.new_tag('p')
                p6.string = str(date['day'])
                p7 = bsObj.new_tag('p')
                p7.string = str(date['month']) + '月' + str(date['day']) + '日'
                p8 = bsObj.new_tag('p')
                p8.string = '星期' + date['week']
                p9 = bsObj.new_tag('p')
                p9.string = date['n_year'] 
                p10 = bsObj.new_tag('p')
                p10.string = date['n_month'] + '月' + date['n_day']  + ' ' + date['jq']
                container3.append(p6)
                container3.append(p7)
                container3.append(p8)
                container3.append(p9)
                container3.append(p10)

                container0.append(img)
                container0.append(container1)
                container0.append(container2)
                container0.append(container3)
                root.append(container0)
        
    with open('douban_{0}_{1}.html'.format(start, end), 'w') as fw:
        fw.write(str(bsObj))


def print_month(index):
    month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    sum = 0

    for i in range(index):
        sum += month_days[i]
    start = sum
    end = sum + month_days[index]
    create_html(start, end)


if __name__ == '__main__':
    #parse_movies()
    #parse_books()
    #parse_dates()
    #create_html(0, 365)
    print_month(1)
    '''
    with open('movies.json', 'r') as f:
        movies = json.loads(f.read())
    with open('books.json', 'r') as f:
        books = json.loads(f.read())
    with open('dates.json', 'r') as f:
        dates = json.loads(f.read())
    movies.extend(books)
    movie_books = movies
    random.shuffle(movie_books)
    with open('movie_book.json', 'w') as f:
        f.write(json.dumps(movie_books))
    '''