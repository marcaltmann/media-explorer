import json

from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig
from sqlalchemy import func, select

from models import Collection, Resource


async def seed_database(sqlalchemy_config: SQLAlchemyAsyncConfig) -> None:
    """Adds some dummy data if no data is present."""
    async with sqlalchemy_config.get_session() as session:
        statement = select(func.count()).select_from(Resource)
        count = await session.execute(statement)
        if not count.scalar():
            with open("seeds/lessons.json") as f:
                lessons = json.load(f)
            with open("seeds/movies.json") as f:
                movies = json.load(f)

            lesson_collection = Collection(name="Chinese Lessons")
            movie_collection = Collection(name="Movies")
            session.add_all([lesson_collection, movie_collection])
            await session.commit()

            for resource in lessons:
                session.add(
                    Resource(
                        name=resource["name"],
                        media_type=resource["media_type"],
                        duration=resource["duration"],
                        url=resource["url"],
                        poster_url=resource["poster_url"],
                        toc=resource["toc"],
                        collection_id=1,
                    )
                )
            for resource in movies:
                session.add(
                    Resource(
                        name=resource["name"],
                        media_type=resource["media_type"],
                        duration=resource["duration"],
                        url=resource["url"],
                        poster_url=resource["poster_url"],
                        toc=resource["toc"],
                        collection_id=2,
                    )
                )
            await session.commit()
