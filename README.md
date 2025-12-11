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

Create a .env file in the project root with the following example:

```env
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=newsdb #do not change if you not sure.
```
---

## Database Structure

Table: news

Stores the quiz news items.

### Create your table
```sql
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    media_type TEXT CHECK (media_type IN ('txt','img','img_txt')) NOT NULL,
    news_type TEXT CHECK (news_type IN ('real','fake')) NOT NULL,
    source TEXT,
    description TEXT,
    file_path TEXT,  -- URL or path to image/media if applicable
    created_at TIMESTAMP DEFAULT now()
);
```
### Quick SQL Commands

Run SQL commands directly inside the database container:
```bash
docker exec -it db psql -U user -d newsdb -c "SQL REQUEST HERE"
```
Example: check all news entries:
```bash
docker exec -it db psql -U user -d newsdb -c "SELECT * FROM news;"
```
For development, you can seed the database with test data using the **backend/scripts/seed_news.py** script.

