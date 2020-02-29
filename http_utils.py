# -*- coding: utf-8 -*-
"""
Http 网络请求工具

Created on Tue Feb 25 15:00:18 2020

@author: GS
"""
import requests
import random
from retrying import retry
import log_utils
import constants


@retry(wait_fixed=3000)
def get_html(url):
    """
    获取Html源码

    :param url: 链接地址 
    :return: html源码
    """
    header = {'Upgrade-Insecure-Requests': '1',
              'User-Agent': constants.USER_AGENTS[random.randint(0, len(constants.USER_AGENTS) - 1)],
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Referer': url,
              'Connection': 'keep-alive',
              'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
              }
    try:
        response = requests.get(url, header)
        return response.text
    
    except Exception as e:
        print(e)
        log_utils.log('./error.log', url + ' ' + str(e))
    
