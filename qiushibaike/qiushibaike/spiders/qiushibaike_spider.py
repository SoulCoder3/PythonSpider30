import lxml
import parsel
import w3lib
import twisted
import cryptography
import scrapy
from qiushibaike.items import QiushibaikeItem


class Qiushibaike(scrapy.Spider):
    name = "qiushibaike"

    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    def start_requests(self):
        urls = [
            "https://www.hacg.sbs/wp/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.header)

    def parse(self, response):
        content_main_div = response.xpath('//*[@id="content"]')
        content_list_article = content_main_div.xpath('./article')
        next_page = response.xpath('//*[@id="content"]/div/*[@class="nextpostslink"]/@href').get()

        for article in content_list_article:
            item = QiushibaikeItem()
            item['title'] = article.xpath('./header/h1/a/text()').get() or 'None'
            item['image'] = article.xpath('./div/p/img').get()
            item['info'] = article.xpath('./div/p/text()').getall()
            item['date'] = article.xpath('./header/div[1]/a/time/text()').get()
            item['url'] = article.xpath('./div/p/a/@href').get()
            yield item


        if next_page is not None and str(next_page).split("/")[-1] != "11":
            yield response.follow(next_page, callback=self.parse)

        '''
        page = response.url.split("/")[-2]
        filename = 'qiushi-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        '''