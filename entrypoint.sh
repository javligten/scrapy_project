#!/bin/bash
# Wait for database to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h db -U postgres; do
  sleep 1
done

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Run spider
echo "Starting spider..."
scrapy crawl property_spider