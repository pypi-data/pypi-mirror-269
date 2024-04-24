"""
@Author: shuangchen
@Time：2024/3/12
@File: selenium.py
@Description: 封装selenium的一些操作，自动获取cookies，隐藏特征
"""

import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class PageNotFound(Exception):
    pass


class SeleniumSpider:
    def __init__(self, url: str, cookies: str = '', headless: bool = True) -> None:
        """
        :param url: 网页链接
        :param cookies: 全局的cookies值
        :param headless: 无头模式
        """
        self.base_url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Cookie': cookies
        }
        self.headless = headless
        self.chrome_path = r'C:\ChromeAutomationProfile'
        if not os.path.exists(self.chrome_path):
            os.mkdir(self.chrome_path)

    def _get_client_cookies(self) -> None:
        """
        获取客户端的cookies
        :return: None
        """
        os.system(f'start chrome --remote-debugging-port=9527 --user-data-dir="{self.chrome_path}"')
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
        chrome = webdriver.Chrome(options=options)
        chrome.get(self.base_url)
        chrome.refresh()
        cookies = ''
        for c in chrome.get_cookies():
            cookies += f'{c["name"]}={c["value"]};'
        self.headers['Cookie'] = cookies

    def get_html(self, url=None) -> str:
        """
        获取网页源码
        :param url: 网页链接
        :return: 网页源码
        """
        if url is None:
            url = self.base_url
        try:
            r = requests.get(url, headers=self.headers)
        except requests.exceptions.ConnectTimeout:
            raise PageNotFound('网页不存在: ' + url)
        else:
            if r.status_code == 412 or r.status_code == 202:
                self._get_client_cookies()
                raise
            elif r.status_code == 404 or r.status_code == 500:
                raise PageNotFound('网页不存在: ' + url)
            r.encoding = 'utf-8'
            return r.text

    def get_content(self, url=None) -> bytes:
        """
        获取文件内容
        :param url: 文件链接
        :return: 文件内容
        """
        if url is None:
            url = self.base_url
        try:
            r = requests.get(url, headers=self.headers)
        except requests.exceptions.ConnectTimeout:
            raise PageNotFound('文件不存在: ' + url)
        else:
            if r.status_code == 412 or r.status_code == 202:
                self._get_client_cookies()
                return self.get_content(url)
            elif r.status_code == 404:
                raise PageNotFound('文件不存在: ' + url)
            return r.content
