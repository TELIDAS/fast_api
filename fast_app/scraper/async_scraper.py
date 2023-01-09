import httpx
import asyncio
from parsel import Selector

from fast_app.db import models
from fast_app.db.database import Database


class AutoRiaScraper:
    START_URL = "https://auto.ria.com/car/used/?page={}"
    TEXT = httpx.get(START_URL).text
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

    async def get_all_pages(self) -> None:
        for page in range(1, 10):
            self.all_pages.append(self.START_URL.format(page))
            for item in self.all_pages:
                self.all_auto_url.extend(
                    self.SELECTOR.xpath(self.ALL_AUTO_URL).extract()
                )

    async def get_http_req(self, client, url):
        resp = await client.get(url)
        if resp is not None:
            # print(resp.text)
            await self.parse(resp.text)
            return resp

    async def parse_data(self) -> None:
        tasks = []
        async with httpx.AsyncClient() as client:
            for auto in self.all_auto_url:
                task = asyncio.ensure_future(self.get_http_req(client, auto))
                resp = tasks.append(task)

            data_dict_gather = await asyncio.gather(*tasks)
            # for data in data_dict_gather:
            #     print(data)
            await client.aclose()

    async def parse(self, html_text):

        # new_text = asyncio.create_task(self.get_http_req(client, auto))
        new_selector = Selector(text=html_text)
        link = new_selector.xpath(self.LINK).get()
        title = new_selector.xpath(self.TITLE).get()
        usd_price = new_selector.xpath(self.USD_PRICE).get()
        mile_age = new_selector.css(self.MILE_AGE).get()
        username = new_selector.xpath(self.USERNAME).extract_first()
        img_url = new_selector.xpath(self.IMAGE_URL).get()
        finder_total = new_selector.xpath(self.TOTAL_IMAGE_COUNT).get()

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
        if usd_price is not None:
            usd_price = int(usd_price[:-1].replace(" ", ""))
        if mile_age is not None:
            mile_age = int(mile_age + "000")
        data_dict = {
            "url": link,
            "title": title,
            "usd_price": usd_price,
            "mile_age": mile_age,
            "username": username,
            "img_url": img_url,
            "img_total_count": img_total_count,
            "car_number": car_number,
        }
        print(data_dict)

        # data = models.Auto(
        #     url=link,
        #     title=title,
        #     usd_price=usd_price,
        #     mile_age=mile_age,
        #     username=username,
        #     img_url=img_url,
        #     img_total_count=img_total_count,
        #     car_number=car_number,
        # )
        # self.database.save_objects(objects=data)

    async def main(self) -> None:
        await self.get_all_pages()
        await self.parse_data()


if __name__ == "__main__":
    scraper = AutoRiaScraper()
    asyncio.run(scraper.main())
