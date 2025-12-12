import os
import asyncio
import sqlalchemy
from databases import Database
from dotenv import load_dotenv
from sqlalchemy import text

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# выбираем файл .env по APP_ENV
app_env = os.getenv("APP_ENV", "local")
dotenv_file = os.path.join(BASE_DIR, ".env.docker" if app_env == "docker" else ".env.local")
load_dotenv(dotenv_file)

user = os.getenv("POSTGRES_USER", "user")
password = os.getenv("POSTGRES_PASSWORD", "pass")
db_name = os.getenv("POSTGRES_DB", "newsdb")
host = os.getenv("POSTGRES_HOST")
if not host:
    host = "db" if app_env == "docker" else "localhost"

DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{db_name}"
database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

news = sqlalchemy.Table(
    "news",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("headline", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("body", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("format", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("is_real", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("media_url", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("summary", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("source_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
)

# тестовые новости
news_data = [
    {
        "headline": "Реальная новость №1",
        "body": "Президент выступил с важным заявлением по экономике.",
        "format": "txt",
        "is_real": True,
        "media_url": None,
        "summary": "Краткое описание реальной новости №1",
        "source_name": "CNN",
    },
    {
        "headline": "Фейковая новость №2",
        "body": "СМИ сообщают о сенсационном открытии, которого не было.",
        "format": "txt",
        "is_real": False,
        "media_url": None,
        "summary": "Описание фейковой новости №2",
        "source_name": "example.com",
    },
    {
        "headline": "Реальная новость с фото №3",
        "body": None,
        "format": "img",
        "is_real": True,
        "media_url": "https://i.postimg.cc/3xN0HJkq/Arc-2025-12-11-23-51-04.png",
        "summary": "Описание реальной новости с фото №3",
        "source_name": "BBC",
    },
    {
        "headline": "Фейковая новость с фото №4",
        "body": None,
        "format": "img",
        "is_real": False,
        "media_url": "https://i.postimg.cc/3xN0HJkq/Arc-2025-12-11-23-51-04.png",
        "summary": "Описание фейковой новости с фото №4",
        "source_name": "TrustMeBro",
    },
    {
        "headline": "Реальная новость с текстом и фото №5",
        "body": "Новый проект стартовал в Европе.",
        "format": "img_txt",
        "is_real": True,
        "media_url": "https://i.postimg.cc/3xN0HJkq/Arc-2025-12-11-23-51-04.png",
        "summary": "Описание реальной новости №5",
        "source_name": "Reuters",
    },
    {
        "headline": "Фейковая новость с текстом и фото №6",
        "body": "Слухи о марсианской колонии оказались фейком.",
        "format": "img_txt",
        "is_real": False,
        "media_url": "https://i.postimg.cc/3xN0HJkq/Arc-2025-12-11-23-51-04.png",
        "summary": "Описание фейковой новости №6",
        "source_name": "FakeNews.com",
    },
]

async def main():
    confirm = input("Стереть всю таблицу и вставить тестовые данные? (y/N): ")
    if confirm.lower() != "y":
        print("Отмена")
        return

    await database.connect()

    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.drop_all(engine)
    metadata.create_all(engine)

    query = news.insert()
    await database.execute_many(query=query, values=news_data)

    await database.disconnect()
    print("Готово!")

if __name__ == "__main__":
    asyncio.run(main())