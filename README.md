# Panoramble Project

## Getting Started

## 1. Docker

You need Docker for work with this project
### Start the services

```bash
docker-compose up -d
```
This will start the backend, Postgres database, and other services defined in docker-compose.yml.

### Stop the services
```bash
docker-compose down
```

---

## 3. Environment Variables

Create `.env.local` and `.env.docker` files in the project root.

### `.env.local` (for running locally)

```env
APP_ENV=local

POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=newsdb
POSTGRES_HOST=localhost
```

### `.env.docker` (for running inside Docker)

```env
APP_ENV=docker

POSTGRES_USER=docker_user
POSTGRES_PASSWORD=docker_pass
POSTGRES_DB=newsdb
POSTGRES_HOST=db
```
---

## Database Structure

Table: newsdb

Stores the quiz news items.

### Create your table
```sql
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    headline TEXT NOT NULL,
    body TEXT,
    format TEXT CHECK (format IN ('txt','img','img_txt')) NOT NULL,
    is_real BOOLEAN NOT NULL,
    media_url TEXT,
    summary TEXT,
    source_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
### Quick SQL Commands

Run SQL commands directly inside the database container:
```bash
docker exec -it db psql -U {user} -d newsdb -c "SQL REQUEST HERE"
```
Example: check all news entries:
```bash
docker exec -it db psql -U {user} -d newsdb -c "SELECT * FROM news;"
```
For development, you can seed the database with test data using the **backend/scripts/seed_news.py** script.

