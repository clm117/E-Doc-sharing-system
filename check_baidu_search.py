#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查百度搜索结果的HTML结构
"""

import requests
from bs4 import BeautifulSoup

# 测试搜索关键词
keyword = "Python site:tieba.baidu.com"

# 百度搜索URL
import urllib.parse
encoded_query = urllib.parse.quote(keyword)
url = f"https://www.baidu.com/s?wd={encoded_query}&ie=utf-8&rn=10"

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://www.baidu.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1'
}

try:
    # 发送请求
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    
    # 保存HTML到文件，方便查看
    with open("baidu_search.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print(f"百度搜索页面HTML已保存到 baidu_search.html")
    
    # 解析HTML，查看搜索结果结构
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 打印页面标题
    print(f"页面标题: {soup.title.text if soup.title else '无标题'}")
    
    # 查找可能的搜索结果容器
    print("\n=== 查找搜索结果容器 ===")
    
    # 尝试不同的选择器
    containers = [
        soup.find_all('div', class_='result'),
        soup.find_all('div', class_='result-op'),
        soup.find_all('div', class_='c-container'),
        soup.find_all('div', class_='c-result'),
        soup.find_all('div', id='content_left'),
        soup.find_all('div', class_='s_tab')
    ]
    
    for i, container in enumerate(containers):
        print(f"容器 {i+1} 找到 {len(container)} 个元素")
    
    # 查看页面中的所有div类名，了解页面结构
    print("\n=== 页面中所有div类名 ===")
    div_classes = set()
    for div in soup.find_all('div'):
        if 'class' in div.attrs:
            for cls in div['class']:
                div_classes.add(cls)
    
    for cls in sorted(div_classes):
        print(cls)
    
    # 查看搜索结果数量
    print("\n=== 搜索结果数量 ===")
    result_count_elem = soup.find('span', class_='nums_text')
    if result_count_elem:
        print(f"搜索结果数量: {result_count_elem.text}")
    
    # 查找所有链接，看看是否有百度贴吧的链接
    print("\n=== 页面中的百度贴吧链接 ===")
    links = soup.find_all('a')
    tieba_links = []
    
    for i, link in enumerate(links):
        if link and 'href' in link.attrs:
            href = link['href']
            if 'tieba.baidu.com' in href:
                tieba_links.append((link.text.strip(), href))
    
    print(f"共找到 {len(tieba_links)} 个百度贴吧链接")
    
    # 打印前10个百度贴吧链接
    for i, (title, href) in enumerate(tieba_links[:10]):
        print(f"{i+1}. {title}: {href}")
        
    # 尝试直接获取content_left下的所有div
    print("\n=== content_left下的所有div ===")
    content_left = soup.find('div', id='content_left')
    if content_left:
        for i, div in enumerate(content_left.find_all('div')):
            print(f"div {i+1} 类名: {div.get('class', [])}")
            if i < 5:  # 只打印前5个div的内容预览
                print(f"  内容预览: {div.text[:100]}...")
            
except Exception as e:
    print(f"发生错误: {str(e)}")
