import scrapy


class BrandItem(scrapy.Item):
    brands = scrapy.Field()
