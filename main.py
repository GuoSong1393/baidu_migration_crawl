# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:50:00 2020

@author: GS
"""      
import get_data as gd
import time

#查看城市编号
#print(gd.CITY_NUM)

if __name__ == "__main__":
    
    #gd.get_migration_city('20200101', '20200101', '唐山市','move_out') 
    #gd.get_migration_province('20200101', '20200101', '北京市','move_out')
    #gd.get_internal_flow('北京市')
    #gd.get_migration_index('北京市', 'move_out')

    city_lst = list(gd.CITY_NUM.keys())
    for city in city_lst:
        gd.get_migration_city('20200101', '20200225', city,'move_in')
        time.sleep(1)

        gd.get_migration_city('20200101', '20200225', city,'move_out')
        time.sleep(1)
        
        gd.get_migration_province('20200101', '20200225', city,'move_in')
        time.sleep(1)
        
        gd.get_migration_province('20200101', '20200225', city,'move_out')
        time.sleep(1)
        
        gd.get_migration_index(city, 'move_in')
        gd.get_migration_index(city, 'move_out')
        
        #只有城市才有城内出行强度,省级没有
        num = gd.CITY_NUM[city]
        if num%10000!=0:
            gd.get_internal_flow(city)
        time.sleep(1)
