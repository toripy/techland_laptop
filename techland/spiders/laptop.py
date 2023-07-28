import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LaptopSpider(CrawlSpider):
    name = "laptop"
    start_urls = [
        "https://www.techlandbd.com/shop-laptop-computer/brand-laptops?limit=100"]

    rules = (Rule(LinkExtractor(
        restrict_xpaths='//div[@class="product-thumb"]/div[@class="caption"]/div[@class="name"]/a'), callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="next"]'), follow=True)

    )

    def parse_item(self, response):
        details = response.xpath('//div[@class="product-details"]//tr')
        product_price = "Not available"
        special_price = "Not available"
        brand_name = None

        for index, feature in enumerate(details, 1):

            # product price, special price, brand name
            if response.xpath(f'((//div[@class="product-details"]//tr)[{index}]/td)[1]/text()').get().strip().casefold() == 'Product Price'.casefold():
                product_price = int(response.xpath(
                    f'((//div[@class="product-details"]//tr)[{index}]/td)[2]/text()').get().strip().replace('৳', '').replace(',', ''))

            if response.xpath(f'((//div[@class="product-details"]//tr)[{index}]/td)[1]/text()').get().strip().casefold() == 'Special Price'.casefold():
                special_price = int(response.xpath(
                    f'((//div[@class="product-details"]//tr)[{index}]/td)[2]/text()').get().strip().replace('৳', '').replace(',', ''))

            if response.xpath(f'((//div[@class="product-details"]//tr)[{index}]/td)[1]/text()').get().strip().casefold() == 'Brand'.casefold():
                brand_name = response.xpath(
                    f'((//div[@class="product-details"]//tr)[{index}]/td)[2]/a/text()').get().strip()

        # emi price
        emi_price = None
        try:
            emi_price = int(response.xpath(
                '//div[@class="module-item module-item-2 no-expand"]//span[@class="block-header-text"]/text()').get().strip().replace('৳', '').replace(',', ''))
        except:
            emi_price = 'Not available'

        features = response.xpath('//td[@class="attribute-name"]')
        processor = 'Not available'
        memory = 'Not available'
        storage = 'Not available'
        graphics = 'Not available'
        display = 'Not available'
        for index, feature in enumerate(features, 1):

            if response.xpath(f'(//td[@class="attribute-name"])[{index}]/text()') .get().strip().casefold() == 'Processor'.casefold():
                processor = ' '.join(response.xpath(
                    f'(//td[@class="attribute-value"])[{index}]/text()').get().split())

            elif response.xpath(f'(//td[@class="attribute-name"])[{index}]/text()') .get().strip().casefold() == 'Memory'.casefold():
                memory = ' '.join(response.xpath(
                    f'(//td[@class="attribute-value"])[{index}]/text()').get().split())

            elif response.xpath(f'(//td[@class="attribute-name"])[{index}]/text()') .get().strip().casefold() == 'Storage'.casefold():
                storage = ' '.join(response.xpath(
                    f'(//td[@class="attribute-value"])[{index}]/text()').get().split())

            elif response.xpath(f'(//td[@class="attribute-name"])[{index}]/text()') .get().strip().casefold() == 'Graphics'.casefold():
                graphics = ' '.join(response.xpath(
                    f'(//td[@class="attribute-value"])[{index}]/text()').get().split())

            elif response.xpath(f'(//td[@class="attribute-name"])[{index}]/text()') .get().strip().casefold() == 'Display'.casefold():
                display = ' '.join(response.xpath(
                    f'(//td[@class="attribute-value"])[{index}]/text()').get().split())

        yield dict(

            title=' '.join(response.xpath(
                '//caption/div[@class="title page-title"]/text()').get().split()),
            brand_name=brand_name,
            processor=processor,
            memory=memory,
            storage=storage,
            display=display,
            product_price=product_price,
            special_price=special_price,
            emi_price=emi_price,
            url=response.url
        )
