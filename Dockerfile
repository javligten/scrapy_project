FROM python:3.10-slim

WORKDIR /scrapy_project/scrapy_project

# Install PostgreSQL client for pg_isready
RUN apt-get update && apt-get install -y postgresql-client

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Make entrypoint script executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Use entrypoint script
ENTRYPOINT ["./entrypoint.sh"]