import random
import requests
from scrapy import signals
from fake_useragent import UserAgent

class AllegroScraperSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class AllegroScraperDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class RotateUserAgentMiddleware:
    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.ua.random)


class ProxyMiddleware:
    def __init__(self):
        self.proxies = self.get_proxies()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        if self.proxies:
            proxy = random.choice(self.proxies)
            request.meta['proxy'] = proxy

    def get_proxies(self):
        proxy_api_url = 'https://www.proxy-list.download/api/v1/get?type=https'
        response = requests.get(proxy_api_url)
        proxies = response.text.split('\r\n')
        valid_proxies = self.validate_proxies(proxies)
        return valid_proxies

    def validate_proxies(self, proxies):
        valid_proxies = []
        test_url = 'https://httpbin.org/ip'
        headers = {'User-Agent': UserAgent().random}
        for proxy in proxies:
            try:
                response = requests.get(test_url, proxies={'http': proxy, 'https': proxy}, headers=headers, timeout=5)
                if response.status_code == 200:
                    valid_proxies.append(proxy)
            except Exception as e:
                continue
        return valid_proxies


class ProxyUpdater:
    @classmethod
    def from_crawler(cls, crawler):
        updater = cls()
        crawler.signals.connect(updater.update_proxies, signal=signals.spider_opened)
        crawler.signals.connect(updater.update_proxies, signal=signals.spider_idle)
        return updater

    def update_proxies(self):
        proxy_middleware = ProxyMiddleware()
        proxy_middleware.proxies = proxy_middleware.get_proxies()
