import asyncio
import databases
import sqlalchemy

DATABASE_URL = "postgresql://user:pass@localhost:5432/newsdb"  # подставь свои

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

news = sqlalchemy.Table(
    "news",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("content", sqlalchemy.Text),
    sqlalchemy.Column("media_type", sqlalchemy.String),
    sqlalchemy.Column("news_type", sqlalchemy.String),
    sqlalchemy.Column("source", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("file_path", sqlalchemy.String),
)

# список новостей
news_data = [
    {
        "title": "Трамп обещает остановить войну",
        "content": "Президент США заявил ...",
        "media_type": "txt",
        "news_type": "real",
        "source": "CNN",
        "description": "Короткое описание",
        "file_path": None,
    },
    {
        "title": "Сперма донора с мутированным геном",
        "content": "Использована для зачатия почти 200 детей",
        "media_type": "txt",
        "news_type": "fake",
        "source": "SomeSource",
        "description": "Описание новости",
        "file_path": None,
    },
]

async def main():
    await database.connect()
    query = news.insert()
    await database.execute_many(query=query, values=news_data)
    await database.disconnect()

if __name__ == "__main__":
    asyncio.run(main())