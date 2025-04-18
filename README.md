
# Property Data Scraper

This project scrapes real estate property data from [mva.nl](https://mva.nl) and organizes it using Object-Oriented Programming (OOP) principles. It then stores it in a PostgreSQL database that is normalized to 3NF (Third Normal Form).

## Features

- Extracts the following data from property listings:
  - Price
  - Status (e.g., for rent, rented out, under option) – with normalized status mapping
  - Number of rooms
  - Property type
  - Features (e.g., garden, parking) – filtering out fixed properties like price and surface area to avoid duplication
  - Agent information
  - Property images – with validation of image URLs
- Scrapes multiple pages of property listings using Scrapy’s pagination support
- Uses [Scrapy](https://scrapy.org/) for web scraping
- Uses [SQLAlchemy](https://www.sqlalchemy.org/) ORM to store data in a PostgreSQL database
- Dockerized for easy setup and deployment
- Implements type hints for better code readability and maintainability

## Setup

### 1. Clone the repository

```bash
git clone <your-local-path>
cd scrapy_project
```

### 2. Set up Docker

This project is dockerized, meaning you can set up the environment easily using Docker.

1. Ensure you have [Docker](https://www.docker.com/get-started) installed on your system.
2. Build the Docker containers by running the following command:

```bash
docker compose up --build
```

3. Once the containers are built, you can access the PostgreSQL database:

```bash
docker compose run db psql -U postgres -d scrapy_db
```

### 3. Configure Database

The `docker-compose.yml` file should automatically handle starting the PostgreSQL database container for you. When you run `docker compose up --build`, the database container will be created and started automatically.

### 4. Running the Scraper

To start the scraping process:

```bash
docker compose exec scrapy_project scrapy crawl property_spider
```

This will start the Scrapy spider to scrape the property data across multiple pages.

## Improvements

- **Status Mapping**: Property status values (e.g., "under_option", "for_rent", "rented_out") are mapped to standardized values.
- **Filtering Duplicate Values**: Fixed properties like price and surface area are no longer stored as part of the features to avoid duplicates.
- **Pagination Support**: The spider can now scrape multiple pages of property listings, automatically following links to the next page.
- **Image URL Validation**: The scraper checks if the image URLs are valid before storing them in the database.
- **Type Hints**: Python type hints have been added to the spider code for improved clarity and easier maintenance.

## Notes

- Data will be stored in the PostgreSQL database, which will be accessible through the Docker container.
- You may want to adjust the `scrapy_project/settings.py` file if you need to modify scraping behaviors such as the number of concurrent requests, download delay, etc.
- The scraper will continue crawling through multiple pages of listings until no more next-page links are found.

## Dependencies

- Python 3
- Scrapy
- SQLAlchemy
- PostgreSQL
- Docker
