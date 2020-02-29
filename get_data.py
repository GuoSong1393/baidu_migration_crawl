# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:50:00 2020

@author: GS
"""

import csv
import json
import pandas as pd
from datetime import datetime, timedelta
import http_utils
import constants

CITY_RANK_BASE_URL = constants.CITY_RANK_BASE_URL
PROVINCE_RANK_BACE_URL = constants.PROVINCE_RANK_BACE_URL
INTERNAL_FLOW_BACE_URL = constants.INTERNAL_FLOW_BACE_URL
MIGRATION_INDEX_BACE_URL = constants.MIGRATION_INDEX_BACE_URL
CITY_NUM = constants.CITY_NUM


def get_migration_city(startDate, endDate, city, move_type):
    
    """
    获取市级迁移数据

    :param startDate: 开始时间
    :param endDate：结束时间
    :param city：城市或者省
    :param move_type：迁移类型（move_in;move_out）
    :return: none
    """
    
    apiUrl = CITY_RANK_BASE_URL + 'dt=city&id=' + str(CITY_NUM[city]) + '&type=' + move_type + '&date={}'
    date = datetime.strptime(startDate, "%Y%m%d")
    end = datetime.strptime(endDate, "%Y%m%d")
    print(city)
    final_list = []
    while date <= end:
        currentDate = date.strftime('%Y%m%d')
        print(currentDate)
        date = date + timedelta(days=1)
        
        url = apiUrl.format(currentDate)
        print(url)
        
        restext = http_utils.get_html(url)

        migration_data = json.loads(restext[3:-1])['data']['list']
        
        result = [currentDate, city]
        for data in migration_data:
            result.append(data['city_name'])
            result.append(data['value'])
        final_list.append(result)
    if move_type == 'move_out':
        city1 = 'from_city'
        city2 = 'to_city'
    else:
        city1 = 'to_city'
        city2 = 'from_city'
    with open('./data/' + city + '_' + move_type + '_migration_city.csv', 'w', encoding='utf-8-sig', newline='') as outFileCsv:
        writer = csv.writer(outFileCsv)
        # 表头
        result = ['date', city1]
        for i in range(1, 101):
            result.append(city2+str(i))
            result.append('ratio'+str(i))
        writer.writerow(result)
        writer = csv.writer(outFileCsv)
        # 数据
        writer.writerows(final_list)
        print(city + '_' + move_type + '_migration_city.csv' + ' have been saved!')
        

def get_migration_province(startDate, endDate, city, move_type):
    
    """
    获取省级迁移数据

    :param startDate: 开始时间
    :param endDate：结束时间
    :param city：城市或者省
    :param move_type：迁移类型（move_in;move_out）
    :return: none
    """
    
    date = datetime.strptime(startDate, "%Y%m%d")
    end = datetime.strptime(endDate, "%Y%m%d")
    final_list = []
    print(city)
    while date <= end:
        
        currentDate = date.strftime('%Y%m%d')
        print(currentDate)
        date = date + timedelta(days=1)
        
        url = PROVINCE_RANK_BACE_URL + 'dt=city&id=' + str(CITY_NUM[city]) + '&type=' + move_type + '&date=' + currentDate
        print(url)
        
        restext = http_utils.get_html(url)
        
        migration_data = json.loads(restext[3:-1])['data']['list']
        result = [currentDate, city]
        for data in migration_data:
            result.append(data['province_name'])
            result.append(data['value'])
        final_list.append(result)
    if move_type == 'move_out':
        city1 = 'from_city'
        city2 = 'to_province'
    else:
        city1 = 'to_city'
        city2 = 'from_province'
    with open('./data/' + city + '_' + move_type + '_migration_province.csv', 'w', encoding='utf-8-sig', newline='') as outFileCsv:
        writer = csv.writer(outFileCsv)
        # 表头
        result = ['date', city1]
        for i in range(1, 31):
            result.append(city2+str(i))
            result.append('ratio'+str(i))
        writer.writerow(result)
        writer = csv.writer(outFileCsv)
        # 数据
        writer.writerows(final_list)
        print(city + '_' + move_type +  '_migration_province.csv' + ' have been saved!')
        
        
def get_internal_flow(city):
    """
    获取城市城内出行强度数据

    :param city：只能是城市（只有城市有城内出行强度）
    :return: none
    """
    
    url = INTERNAL_FLOW_BACE_URL + 'dt=city&id=' + str(CITY_NUM[city]) + '&date=20200223'
    print(city)
    print(url)
    
    restext = http_utils.get_html(url)
    internal_flow = json.loads(restext[3:-1])['data']['list']
    
    key = list(internal_flow.keys())
    value = list(internal_flow.values())
    tempdict = {'date':key,'value':value}
    df = pd.DataFrame(tempdict)
    df.to_csv('./data/' + city + '_internal_flow.csv',encoding = 'ANSI', index=False)
    print(city + '_internal_flow.csv' + ' have been saved!')

def get_migration_index(city, move_type):
    """
    获取城市迁徙规模指数

    :param city：城市或者省
    :param move_type：迁移类型（move_in;move_out）
    :return: none
    """
    
    url = MIGRATION_INDEX_BACE_URL + 'dt=city&id=' + str(CITY_NUM[city]) + '&type=' + move_type
    print(city)
    print(url)
    
    restext = http_utils.get_html(url)
    internal_flow = json.loads(restext[3:-1])['data']['list']
    
    key = list(internal_flow.keys())
    value = list(internal_flow.values())
    tempdict = {'date':key,'value':value}
    df = pd.DataFrame(tempdict)
    df.to_csv('./data/' + city + '_' + move_type +'_migration_index.csv',encoding = 'ANSI',index = False)
    print(city + '_' + move_type +'_migration_index.csv' + ' have been saved!')

