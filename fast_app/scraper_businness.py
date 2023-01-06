import requests
from parsel import Selector
# import db_mongo, db_pg
from db.models import Auto
from db.database import Database


class AutoRiaScraper:
    START_URL = "https://auto.ria.com/car/used/?page={}"
    TEXT = requests.get(START_URL).text
    SELECTOR = Selector(text=TEXT)
    LINK = '//head/link[@rel="amphtml"]/@href'
    TITLE = "//h1/text()"
    USD_PRICE = "//div[@class='price_value']/strong/text()"
    MILE_AGE = "span.size18::text"
    USERNAME = '//div[@class="seller_info_name bold"]/text()'
    ALT_USERNAME = '//h4[@class="seller_info_name"]/a/strong/text()'
    PHONE = "div.popup-successful-call-desk.size24.bold.green.mhide.green::text"
    IMAGE_URL = '//div[contains(@class, "carousel-inner")]/div[1]//img/@src'
    TOTAL_IMAGE_COUNT = '//span[@class="count"]/span[@class="mhide"]/text()'
    CAR_NUMBER = '//span[@class="state-num ua"]/text()'
    VIN_CODE = '//span[@class="vin-code"]//text()'
    ALT_VIN_CODE = "//span[@class='label-vin']//text()"
    ALL_AUTO_URL = '//a[@class="address"]/@href'
    ALLOW_STATUS_CODES = [200]
    RETRIES = 5

    def __init__(self) -> None:
        self.database = Database()
        self.all_pages = []
        self.all_auto_url = []

    def get_all_pages(self) -> None:
        for page in range(1, 21):
            self.all_pages.append(self.START_URL.format(page))
            for item in self.all_pages:
                self.all_auto_url.extend(
                    self.SELECTOR.xpath(self.ALL_AUTO_URL).extract()
                )

    def parse_data(self) -> None:
        for auto in self.all_auto_url:
            new_text = requests.get(auto).text
            new_selector = Selector(text=new_text)
            link = new_selector.xpath(self.LINK).get()
            title = new_selector.xpath(self.TITLE).get()
            usd_price = new_selector.xpath(self.USD_PRICE).get()
            mile_age = new_selector.css(self.MILE_AGE).get()
            username = new_selector.xpath(self.USERNAME).extract_first()
            img_url = new_selector.xpath(self.IMAGE_URL).get()
            finder_total = new_selector.xpath(self.TOTAL_IMAGE_COUNT).get()
            if len(mile_age) > 25:
                mile_age = None
            if username is not None:
                username = new_selector.xpath(self.USERNAME).extract_first()
            else:
                username = new_selector.xpath(self.ALT_USERNAME).extract_first()
            if finder_total is not None:
                img_total_count = finder_total[3:]
            else:
                img_total_count = None
            car_number = new_selector.xpath(self.CAR_NUMBER).get()
            vin_code = "".join(new_selector.xpath(self.VIN_CODE).extract())
            if vin_code == "":
                vin_code = "".join(new_selector.xpath(self.ALT_VIN_CODE).extract())

            data = {
                "url": link,
                "title": title,
                "usd_price": int(usd_price[:-1].replace(" ", "")),
                "mile_age": int(mile_age + "000"),
                "username": username,
                "img_url": img_url,
                "img_total_count": img_total_count,
                "car_number": car_number,
            }
            # db_mongo.log(data=data)
            print(data)

            data = Auto(
                url=link,
                title=title,
                usd_price=int(usd_price[:-1].replace(" ", "")),
                mile_age=int(mile_age + "000"),
                username=username,
                img_url=img_url,
                img_total_count=img_total_count,
                car_number=car_number,
            )
            self.database.save_objects(objects=data)

    def main(self) -> None:
        self.get_all_pages()
        self.parse_data()


if __name__ == "__main__":
    scraper = AutoRiaScraper()
    scraper.main()
