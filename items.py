import scrapy

class PropertyItem(scrapy.Item):
    price = scrapy.Field()
    rental_status = scrapy.Field()
    num_rooms = scrapy.Field()
    num_bedrooms = scrapy.Field()
    property_type = scrapy.Field()
    surface_area = scrapy.Field()
    features = scrapy.Field()
    image_urls = scrapy.Field()
    agent_name = scrapy.Field()
    agent_phone = scrapy.Field()
    agent_email = scrapy.Field()
