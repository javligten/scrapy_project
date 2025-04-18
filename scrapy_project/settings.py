import os

# Scrapy settings for scrapy project
BOT_NAME = 'scrapy_project'

SPIDER_MODULES = ['scrapy_project.spiders']
NEWSPIDER_MODULE = 'scrapy_project.spiders'

USER_AGENT = 'scrapy_project (+http://www.yourdomain.com)'

ROBOTSTXT_OBEY = True

# PostgreSQL settings (for pipelines)
DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://postgres:password@db:5432/scrapy_db")

# Enabling pipeline
ITEM_PIPELINES = {
    'scrapy_project.pipelines.PostgresPipeline': 1,
}
