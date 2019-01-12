# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 16:05:52 2018
 
@author: pwang18
"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pykrige.kriging_tools as kt
from pykrige.ok import OrdinaryKriging
from pykrige.uk import UniversalKriging
import json
import requests
 
def get_aqi():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
            'host': 'zqyjbg.com',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive'
    }
    url = 'https://aqicn.org/mapi/?region=china&lang=cn&key=_2Y2EvEhx2M1kfIy8LSSJWXmpjfAM/LScbFmgvYg==&v=2'
    data = requests.get(url, headers=headers).json()


def wgs84_to_mercator(lon, lat):
    x = lon * 20037508.342789 / 180
    y = np.log(np.tan((90+lat) * np.pi / 360)) / (np.pi/180) 
    y = y * 20037508.342789 / 180
    return [x, y]
    

def create_kriging_img():
    with open('public/AQI/data.json') as f:
        data = json.loads(f.read())
    items = []
    for item in data:
        if item['aqi'].isdigit():
        #if item['aqi'] != '-':
            res = wgs84_to_mercator(float(item['lon']), float(item['lat']))
            items.append([res[0], res[1], item['aqi']])
    items = np.array(items, dtype=np.float32)
    OK = OrdinaryKriging(items[:, 0], items[:, 1], items[:, 2],
                        variogram_model='exponential')
    #gridx = np.arange(73.4766, 135.0879, 0.1)
    #gridy = np.arange(18.1055, 53.5693, 0.1)
    gridx = np.arange(8179377.70, 15037916.24, 10000)
    gridy = np.arange(2049900.84, 7089005.20, 10000)
    z, ss = OK.execute('grid', gridx, gridy)
    implot = plt.imshow(z.data[::-1], cmap='OrRd')
    #plt.colorbar()
    implot.axes.get_xaxis().set_visible(False)
    implot.axes.get_yaxis().set_visible(False)
    plt.axis('off')
    plt.savefig('aqi', bbox_inches='tight', pad_inches=0)
    print('create kriging image successfully')


if __name__ == '__main__':
    get_aqi()
    create_kriging_img()
    
    
    
    
    
    