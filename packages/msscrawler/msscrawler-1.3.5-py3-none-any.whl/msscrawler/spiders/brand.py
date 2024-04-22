from ..items.brand_item import BrandItem
from .base import BaseSpider
import scrapy


class BrandSpider(BaseSpider):
    instance = "brand"

    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)

    @staticmethod
    def get_new_item_instance():
        return BrandItem()

    def set_default_value(self):
        items = self.get_new_item_instance()

        items["brands"] = []
        return items
