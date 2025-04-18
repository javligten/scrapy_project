# Property Data Scraper

This project scrapes real estate property data from [mva.nl](https://mva.nl), organizes it using Object-Oriented Programming (OOP) principles, and stores it in a PostgreSQL database normalized to 3NF (Third Normal Form).

## Features

- Extracts the following data from property listings:
  - Price
  - Status (e.g., for sale, sold)
  - Number of rooms
  - Property type
  - Features (e.g., garden, parking)
  - Agent information
  - Property images
- Uses [Scrapy](https://scrapy.org/) for web scraping
- Uses [SQLAlchemy](https://www.sqlalchemy.org/) ORM to store data in a PostgreSQL database
- Dockerized for easy setup and deployment

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

This will start the Scrapy spider to scrape the property data.

## Notes

- Data will be stored in the PostgreSQL database, which will be accessible via the Docker container.
- You may want to adjust the `scrapy_project/settings.py` file if you need to modify scraping behaviors such as the number of concurrent requests, download delay, etc.

## Dependencies

- Python 3.x
- Scrapy
- SQLAlchemy
- PostgreSQL
- Docker