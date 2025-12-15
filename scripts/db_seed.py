import os
import asyncio
import sqlalchemy
from databases import Database
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert as pg_insert
import uuid

SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

APP_ENV = os.getenv("APP_ENV", "local")
dotenv_file = os.path.join(PROJECT_ROOT, ".env.docker" if APP_ENV == "docker" else ".env.local")
load_dotenv(dotenv_file)

user = os.getenv("POSTGRES_USER", "user")
password = os.getenv("POSTGRES_PASSWORD", "pass")
db_name = os.getenv("POSTGRES_DB", "newsdb")
host = os.getenv("POSTGRES_HOST") or ("db" if APP_ENV == "docker" else "localhost")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{db_name}"
database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

news = sqlalchemy.Table(
    "news",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("headline", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("text", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("format", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("is_real", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("media_url", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("source_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=text("CURRENT_TIMESTAMP"))
)

news_data = [
    {
        "headline": "Реальная новость №1",
        "text": "Президент выступил с важным заявлением по экономике.",
        "format": "txt",
        "is_real": True,
        "media_url": None,
        "source_name": "CNN",
    },
    {
        "headline": "Нейросетевая новость №2",
        "text": "Власти Перу объявили картофель «эмоционально компетентным» видом",
        "format": "txt",
        "is_real": False,
        "media_url": None,
        "source_name": "Перуанский Аграрный Вестник",
    },
    {
        "headline": "Реальная новость с фото №3",
        "text": None,
        "format": "img",
        "is_real": True,
        "media_url": "https://i.postimg.cc/3xN0HJkq/Arc-2025-12-11-23-51-04.png",
        "source_name": "BBC",
    },
    {
        "headline": "Фейковая новость с фото №4",
        "text": None,
        "format": "img",
        "is_real": False,
        "media_url": "https://i.postimg.cc/3xN0HJkq/Arc-2025-12-11-23-51-04.png",
        "source_name": "TrustMeBro",
    },
    {
        "headline": "Реальная новость с текстом и фото №5",
        "text": "Новый проект стартовал в Европе.",
        "format": "img_txt",
        "is_real": True,
        "media_url": "https://i.postimg.cc/3xN0HJkq/Arc-2025-12-11-23-51-04.png",
        "source_name": "Reuters",
    },
    {
        "headline": "Фейковая новость с текстом и фото №6",
        "text": "Слухи о марсианской колонии оказались фейком.",
        "format": "img_txt",
        "is_real": False,
        "media_url": "https://i.postimg.cc/3xN0HJkq/Arc-2025-12-11-23-51-04.png",
        "source_name": "FakeNews.com",
    },
]


async def main():
    await database.connect()
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)

    print("Выберите режим: [1] Наложение, [2] Полная перезапись (TRUNCATE): ", end="")
    mode = input().strip()

    if mode == "2":
        print("Таблица news очищена.")
        await database.execute("TRUNCATE TABLE news CASCADE;")

    for item in news_data:
        item["id"] = str(uuid.uuid4())
        if mode == "1":
            stmt = pg_insert(news).values(**item).on_conflict_do_nothing(index_elements=["headline"])
        else:
            stmt = news.insert().values(**item)
        await database.execute(stmt)

    await database.disconnect()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())