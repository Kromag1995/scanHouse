import scrapy
from scrapy_splash import SplashRequest
from ..items import PropItem

class ArgenpropSpider(scrapy.Spider):
    name = "argenprop"
    allowed_domains = ["www.argenprop.com"]
    start_urls = ["https://www.argenprop.com/departamento-y-casa-y-ph-alquiler-localidad-capital-federal-orden-masnuevos/"]
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

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse, headers=self.HEADERS)

    def parse(self, response):
        urls = response.xpath('//div[has-class("listing__item")]/a/@href').extract()
        next_page = response.xpath('//li[has-class("pagination__page-next")]/a/@href').extract_first()
        for url in urls:
            url = "https://www.argenprop.com" + url
            yield SplashRequest(url, callback=self.parse_prop, headers=self.HEADERS)
        if next_page:
            url = "https://www.argenprop.com" + next_page
            yield SplashRequest(url, callback=self.parse, headers=self.HEADERS)

    def parse_prop(self, response):
        prop_item = PropItem()
        main = response.xpath('//div[has-class("property-main")]')
        price_cont = main.xpath('./div["titlebar__price-mobile"]')
        price = price_cont.xpath('./p/text()').extract_first().strip().split(" ")
        if "precio" in price:
            prop_item["price"] = 0
            prop_item["currency"] = "$"
        else:
            prop_item["price"] = price[1].replace(".", "")
            prop_item["currency"] = price[0]
        expens = price_cont.xpath('./span/text()').extract_first()
        if expens:
            prop_item["expens"] = expens.replace("+", "")\
            .replace("expensas", "")\
            .replace("$", "")\
            .replace(".", "")\
            .strip()
        prop_item["title"] = main.xpath('//p[has-class("section-description--title")]/text()').extract_first().strip()
        location = main.xpath('//div[has-class("titlebar__bottom")]/h2/text()').extract_first()
        if location:
            location = location.split(",")
            big_location = location[1].strip()
            small_location = location[0].split("Alquiler en")[1]
            if big_location == "Capital Federal":
                prop_item["location"] = small_location
            else:
                prop_item["location"] = big_location
        props_feature = main.xpath('//ul[has-class("property-main-features")]')
        m2_cub = props_feature.xpath('//li[@title="Sup. cubierta"]/div[has-class("desktop")]/p/text()')\
            .extract_first()
        if m2_cub:
            prop_item["m2_cub"] = m2_cub.split("m")[0].strip()
            prop_item["m2_total"] = prop_item["m2_cub"]
        bedrooms = props_feature.xpath('//li[@title="Dormitorios"]/div[has-class("desktop")]/p/text()')\
            .extract_first()
        if bedrooms and "monoambiente" in bedrooms.lower():
            prop_item["bedrooms"] = 1
        elif bedrooms:
            prop_item["bedrooms"] = bedrooms.split(" ")[0].strip()
        rooms = props_feature.xpath('//li[@title="Ambientes"]/div[has-class("desktop")]/p/text()')\
            .extract_first()
        if rooms:
            prop_item["rooms"] = rooms.split(" ")[0].strip()
        prop_item["url"] = response.url
        direction = main.xpath("//div[has-class('titlebar')]/h3/text()")\
            .extract_first()
        if direction:
            prop_item["direction"] = direction.strip().lower().capitalize()
        yield prop_item