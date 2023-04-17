import scrapy
from scrapy_splash import SplashRequest
from ..items import PropItem


class ZonapropSpider(scrapy.Spider):
    name = "zonaprop"
    allowed_domains = ["www.zonaprop.com.ar"]
    start_urls = ["https://www.zonaprop.com.ar/casas-departamentos-ph-alquiler-capital-federal-publicado-hace-menos-de-1-semana.html"]
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded"
    }
    props_url = "https://www.zonaprop.com.ar"

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse, headers=self.HEADERS)

    def parse(self, response):
        url_containers = response.xpath('//div[has-class("postings-container")]/div')
        for i in url_containers:
            yield SplashRequest(self.props_url + i.xpath("./div/@data-to-posting").extract_first(),
                                callback=self.parse_prop, headers=self.HEADERS)
        url = response.xpath("//a[@class='sc-n5babu-2 gudFvk']/@href").extract_first()
        if url:
            url = self.props_url + url
            yield SplashRequest(url, callback=self.parse, headers=self.HEADERS)

    def parse_prop(self, response):
        prop_item = PropItem()
        prop_item["url"] = response.url
        prop_item["title"] = response.xpath('//hgroup[has-class("title-container")]/div/h1/text()').extract_first(default="")
        prop_item["direction"] = response.xpath('//hgroup[has-class("title-container")]/h2/text()').extract_first(default="")\
            .replace("\n", "")
        location = response.xpath('//hgroup[has-class("title-container")]/h2/span/text()').extract_first(default="")
        try:
            low_location = location.split(",")[1].strip()
            big_location = location.split(",")[2].strip()
            if big_location == "Capital Federal":
                location = low_location.lower()
            else:
                location = big_location.lower()
        except Exception as e:
            self.logger.error(e)
        prop_item["location"] = location
        price = response.xpath('//div[has-class("price-items")]/span/span/text()').extract_first(default="s n").strip()\
            .split(" ")
        prop_item["price"] = price[1].replace(".", "")
        if prop_item["price"] == "precio":
            prop_item["price"] = 0
        prop_item["currency"] = price[0]
        prop_item["expens"] = response.xpath("//div[has-class('block-expensas')]/span/text()")\
            .extract_first(default="").replace("$", "")
        if not prop_item["expens"]:
            prop_item["expens"] = 0
        props = response.xpath("//ul[has-class('section-icon-features')]/li")
        for prop in props:
            if prop.xpath("./i[has-class('icon-stotal')]"):
                prop_item["m2_total"] = prop.xpath("./text()").extract()[1].strip().split("\n")[0]
            if prop.xpath("./i[has-class('icon-scubierta')]"):
                prop_item["m2_cub"] = prop.xpath("./text()").extract()[1].strip().split("\n")[0]
            if prop.xpath("./i[has-class('icon-ambiente')]"):
                prop_item["rooms"] = prop.xpath("./text()").extract()[1].strip().split("\n")[0]
            if prop.xpath("./i[has-class('icon-dormitorio')]"):
                prop_item["bedrooms"] = prop.xpath("./text()").extract()[1].strip().split("\n")[0]
        yield prop_item
