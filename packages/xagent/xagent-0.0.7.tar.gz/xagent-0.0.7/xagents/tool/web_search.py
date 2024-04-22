import requests
from bs4 import BeautifulSoup
import time
import random

import requests
import chardet
import sys
sys.path.append("../../")
from xagents.tool.core import BaseTool
from agit.common import Parameter
from typing import Any, Callable, Dict, List
from pydantic import BaseModel, Field

from fake_useragent import UserAgent
import time
import re

def get_search_result(url):
    headers = {
        "User-Agent": UserAgent().random,#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        # 使用 chardet 检测网页编码
        encoding = chardet.detect(response.content)['encoding']
        # 设置解码方式
        response.encoding = encoding

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # 解析搜索结果页面，这里以输出标题和链接为例
            soup_text = soup.text
            return soup_text
    except:
        return ""



def sogou_search(query):
    url = f"https://www.sogou.com/web"
    # "http://www.so.com/s?q=keyword"
    # f"https://www.sogou.com/web"
    params = {"query": query}

    headers = {
        "User-Agent": UserAgent().random,
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        # 使用 chardet 检测网页编码
        encoding = chardet.detect(response.content)['encoding']
        # 设置解码方式
        response.encoding = encoding

        # 等待一段随机时间，模拟人类操作
        time.sleep(random.uniform(1, 2))
        sub_page_contents = []
        sub_page_links = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # 解析搜索结果页面，这里以输出标题和链接为例
            soup_text = soup.text# str(soup)
            pattern = r'data-url="(.*?)"'
            urls = re.findall(pattern, soup_text)
            if len(urls) >= 1:
                for url_temp in urls:
                    sub_page_links.append(url_temp)
                    sub_page_contents.append(get_search_result(url_temp))
            else:
                sub_page_links = []
                sub_page_contents.append(soup_text.replace("\n\n",""))

            return sub_page_links, sub_page_contents
        else:
            print(f"Error: Failed to fetch search results (status code {response.status_code})")
            return None, None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None


#
# def baidu_search(keyword):
#     url = "https://www.baidu.com/s"
#     params = {
#         "wd": keyword  # 关键词参数
#     }
#
#     headers = {
#         "User-Agent": UserAgent().random,#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#         "Referer": "https://www.baidu.com/",  # 设置 Referer 头部
#         "Accept-Language": "en-US,en;q=0.9",  # 接受的语言
#     }
#
#     try:
#         # 发送 GET 请求
#         response = requests.get(url, params=params, headers=headers)
#         response.raise_for_status()  # 抛出异常，如果响应码不是 200
#
#         # 使用 chardet 检测网页编码
#         encoding = chardet.detect(response.content)['encoding']
#         # 设置解码方式
#         response.encoding = encoding
#
#         # 等待一段随机时间，模拟人类操作
#         time.sleep(random.uniform(1, 3))
#
#         # 解析 HTML 页面
#         soup = BeautifulSoup(response.text, "html.parser")
#
#         # 提取搜索结果
#         results = []
#         sub_page_contents = []
#         for item in soup.find_all("h3", class_="t"):
#             title = item.get_text()
#             link = item.a["href"]
#             results.append({"title": title, "link": link})
#             sub_page_content = open_web_page(link)
#             sub_page_contents.append(sub_page_content)
#
#         return results, sub_page_contents
#
#     except requests.exceptions.HTTPError as e:
#         print(f"HTTP Error occurred: {e}")
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")
#
#     return None,None


def baidu_search(query):
    url = "https://www.baidu.com/s"
    params = {
        "wd": query  # 关键词参数
    }

    headers = {
        "User-Agent": UserAgent().random,
        # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.baidu.com/",  # 设置 Referer 头部
        "Accept-Language": "en-US,en;q=0.9",  # 接受的语言
    }

    try:
        # 发送 GET 请求
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # 抛出异常，如果响应码不是 200
        # 使用 chardet 检测网页编码
        encoding = chardet.detect(response.content)['encoding']
        # 设置解码方式
        response.encoding = encoding
        # 等待一段随机时间，模拟人类操作
        time.sleep(random.uniform(1, 3))

        # 解析 HTML 页面
        soup = BeautifulSoup(response.text, "html.parser")
        soup_text = str(soup)
        pattern = r'"mu":"(.*?)"'
        urls = re.findall(pattern, soup_text)
        # 提取搜索结果
        results = []
        sub_page_contents = []
        for url in urls:
            sub_page_contents.append(url)

        return sub_page_contents

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return None

# print(fetch_baidu_search_results("江泽民生平"))

web_search_sogou = BaseTool(name="联网查询", description="根据用户提供的输入，通过搜索引擎从网上去查询信息，尤其是实时的信息",
                           parameters=[Parameter(name="query", description="搜索的语句", type="string", required=True)],
                           callable=sogou_search)


# 测试搜索功能
if __name__ == "__main__":
    keyword = "邓小平生平"
    # web_search = WebSearch()
    # search_results = web_search.sogou_search(keyword)
    search_links, search_contents = web_search_sogou.execute(query=keyword)
    print(f"Search results for '{search_links}':")
    print("text:", search_contents)
    # from snippets.logs import ChangeLogLevelContext



