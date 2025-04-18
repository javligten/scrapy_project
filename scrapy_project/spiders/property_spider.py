import scrapy
from scrapy_project.items import PropertyItem
import re

class PropertySpider(scrapy.Spider):
    name = 'property_spider'
    start_urls = ['https://mva.nl/huur/woningen/kruiskade-119-e']

    def parse(self, response):
        item = PropertyItem()

        # Extracting labels and values
        labels = response.xpath('//span[@class="property-characteristics__label"]/text()').getall()
        values = response.xpath('//span[@class="property-characteristics__value tx-b"]/text()').getall()

        # Mapping labels and values to create dictionary
        raw_features = dict(zip(labels, values))
        clean_features = {}

        # Helper function to extract float
        def extract_float(text):
            try:
                return float(re.sub(r'[^\d.]', '', text.replace(',', '.')))
            except:
                return None

        # Map known labels to fields
        item['price'] = extract_float(raw_features.get('Huurprijs', ''))
        item['rental_status'] = raw_features.get('Status')
        item['num_rooms'] = int(extract_float(raw_features.get('Aantal kamers', '0')) or 0)
        item['num_bedrooms'] = int(extract_float(raw_features.get('Aantal slaapkamers', '0')) or 0)
        item['property_type'] = raw_features.get('Type woning')
        item['surface_area'] = extract_float(raw_features.get('Woningoppervlakte', ''))

        # Clean up features
        for k, v in raw_features.items():
            clean_features[k.strip()] = v.strip()

        item['features'] = clean_features

        # Extract agent information
        item['agent_name'] = response.xpath('//div[@class="agent-info"]/h3/text()').get()
        item['agent_phone'] = response.xpath('//div[@class="agent-info"]/p[@class="phone"]/text()').get()
        item['agent_email'] = response.xpath('//div[@class="agent-info"]/p[@class="email"]/a/text()').get()
        item['image_urls'] = [url for url in response.xpath('//img/@src').getall() if 'woning' in url or 'media' in url]

        yield item
