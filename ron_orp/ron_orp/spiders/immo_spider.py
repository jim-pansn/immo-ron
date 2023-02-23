import scrapy
from scrapy.http import Request
from json import loads
from datetime import datetime, date, timedelta
from math import nan

from ron_orp.items import ImmoPost


def to_float_or_nan(number_str):
    try:
        return float(number_str)
    except ValueError:
        return nan

class ImmoSpider(scrapy.Spider):
    name = "immo"
    URL = "https://www.ronorp.net/zuerich/immobilien/"
    hash = None
    page = 1
    headers = {"X-Requested-With": "XMLHttpRequest"}

    def start_requests(self):
        yield Request(url=self.URL, callback=self.add_hash, dont_filter=True)

    def add_hash(self, response, **kwargs):

        self.hash = response.css("input[name='hash']").attrib["value"]
        self.logger.info(f"hash extracted: {self.hash}")

        url_with_hash = self.URL + f"?page={self.page}&hash={self.hash}"

        yield Request(url=url_with_hash, callback=self.parse_content, headers=self.headers)

    def parse_content(self, response, **kwargs):

        self.logger.info(f"parsing pager {self.page}")

        data = loads(response.text)

        total_pages = int(data["pagesArray"]["pages_count"])
        ts = datetime.fromtimestamp(int(data["result"][0]["showed_date"]))

        # only look at posts from the last 7 days
        if self.page < total_pages and ts.date() >= date.today() - timedelta(days=7):
            self.page += 1
            url_with_hash = self.URL + f"?page={self.page}&hash={self.hash}"
            yield Request(url=url_with_hash, callback=self.parse_content, headers=self.headers)

        for posting in data["result"]:
            if posting["type"] == "inserate":
                yield Request(url=posting["detail_url"], callback=self.parse_details, headers=self.headers)
            else:
                self.logger.info("skipping posting")
                self.logger.info(f"type: {posting['type']}")
                self.logger.info(f"advert_type: {posting['advert_type']}")

    def parse_details(self, response, **kwargs):
        data = loads(response.text)
        ad = data["advert"]
        yield ImmoPost(
            id=ad["advert_id"],
            heading=ad["subject"],
            city=ad["city_id"],
            created=datetime.fromtimestamp(int(ad["created"])),
            text=ad["message"],
            published=datetime.fromtimestamp(int(ad["published"])),
            address=ad["sp_realty_address"],
            limited=ad["sp_realty_contract_limited"],
            zip_code=ad["sp_realty_plz"],
            price=to_float_or_nan(ad["sp_realty_price"]),
            rooms=to_float_or_nan(ad["sp_realty_rooms"]),
            area=ad["sp_realty_stadt_agglo"],
            type=ad["sp_realty_type"],
            view_count_unique=ad["view_count_unique"],
            url=response.url,
        )
