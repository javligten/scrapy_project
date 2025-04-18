import scrapy
from scrapy_project.items import PropertyItem
import re
from urllib.parse import urlparse
from typing import Optional, Generator


class PropertySpider(scrapy.Spider):
    name = 'property_spider'

    # Starting page
    start_urls = ['https://mva.nl/huur/woningen/kruiskade-119-e']

    IGNORE_FEATURES = {
        'Huurprijs', 'Status', 'Aantal kamers',
        'Aantal slaapkamers', 'Type woning', 'Woningoppervlakte'
    }

    STATUS_MAPPING = {
        'Beschikbaar': 'for_rent',
        'Verhuurd': 'rented_out',
        'Onder optie': 'under_option'
    }

    def is_valid_url(self, url: str) -> bool:
        """Checks for valid URL."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def extract_float(self, text: str) -> Optional[float]:
        """Tries to extract float from text or returns None."""
        try:
            clean = text.replace('.', '').replace(',', '.')
            return float(re.sub(r'[^\d.]', '', clean))
        except Exception:
            return None

    def parse(self, response: scrapy.http.Response) -> Generator[PropertyItem, None, None]:
        """Scrape the data of the property."""
        item = PropertyItem()

        labels = response.xpath('//span[@class="property-characteristics__label"]/text()').getall()
        values = response.xpath('//span[@class="property-characteristics__value tx-b"]/text()').getall()
        raw_features = dict(zip(labels, values))
        clean_features = {}
        ignore_features = self.IGNORE_FEATURES.copy()

        # Assign fields and normalization
        item['price'] = self.extract_float(raw_features.get('Huurprijs', ''))

        raw_status = raw_features.get('Status', '').strip()

        if raw_status in self.STATUS_MAPPING:
            item['rental_status'] = self.STATUS_MAPPING[raw_status]
            ignore_features.add('Status')

        elif re.match(r'\d{1,2}-\d{1,2}-\d{4}', raw_status):
            item['rental_status'] = None
            clean_features['Status'] = f"Onder optie tot {raw_status}"
        else:
            item['rental_status'] = 'onbekend'
            ignore_features.add('Status')

        item['num_rooms'] = int(self.extract_float(raw_features.get('Aantal kamers', '0')) or 0)
        item['num_bedrooms'] = int(self.extract_float(raw_features.get('Aantal slaapkamers', '0')) or 0)
        item['property_type'] = raw_features.get('Type woning')
        item['surface_area'] = self.extract_float(raw_features.get('Woningoppervlakte', ''))

        # Additional features
        for k, v in raw_features.items():
            if k not in ignore_features:
                value = v.strip()
                if re.fullmatch(r'[a-zA-Z\s²³]+', value):
                    value = 'onbekend'
                if value:
                    clean_features[k.strip()] = value

        item['features'] = clean_features

        # Agent info
        item['agent_name'] = response.xpath('//div[@class="agent-info"]/h3/text()').get()
        item['agent_phone'] = response.xpath('//div[@class="agent-info"]/p[@class="phone"]/text()').get()
        item['agent_email'] = response.xpath('//div[@class="agent-info"]/p[@class="email"]/a/text()').get()

        # Check for valid URLs
        raw_urls = response.xpath('//img/@src').getall()
        item['image_urls'] = [
            url for url in raw_urls
            if ('woning' in url or 'media' in url) and self.is_valid_url(url)
        ]

        yield item

        # Search for link to the next page
        next_page = response.xpath('//a[contains(@class, "next")]/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
