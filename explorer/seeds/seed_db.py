import json
from pathlib import Path

from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig
from sqlalchemy import func, select

from explorer.models import Collection, Resource, Category


async def seed_database(sqlalchemy_config: SQLAlchemyAsyncConfig) -> None:
    """Adds some dummy data if no data is present."""
    async with sqlalchemy_config.get_session() as session:
        statement = select(func.count()).select_from(Resource)
        count = await session.execute(statement)
        if not count.scalar():
            with open(Path(__file__).parent / 'lessons.json') as f:
                lessons = json.load(f)
            with open(Path(__file__).parent / 'movies.json') as f:
                movies = json.load(f)

            lesson_collection = Collection(name='Chinese Lessons')
            movie_collection = Collection(name='Movies')
            session.add_all([lesson_collection, movie_collection])
            await session.commit()

            movie_category = Category(name='Movie')
            lesson_category = Category(name='Lesson')
            feature_category = Category(name='Feature film')
            session.add_all([movie_category, lesson_category, feature_category])
            await session.commit()

            for resource in lessons:
                session.add(
                    Resource(
                        name=resource['name'],
                        toc=resource['toc'],
                        is_published=resource['is_published'],
                        collection_id=1,
                        categories=[lesson_category],
                    )
                )
            for resource in movies:
                session.add(
                    Resource(
                        name=resource['name'],
                        toc=resource['toc'],
                        is_published=resource['is_published'],
                        collection_id=2,
                        categories=[movie_category, feature_category],
                    )
                )
            await session.commit()
