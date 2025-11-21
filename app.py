from pathlib import Path
import json

from jinja2 import Environment, PackageLoader, select_autoescape
from litestar import Litestar, get
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig
from sqlalchemy import func, select

from controllers.page_controller import PageController
from controllers.collection_controller import CollectionController
from controllers.resource_controller import ResourceController
from models import Collection, Resource


session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///test.sqlite",
    session_config=session_config,
    create_all=True,
)  # Create 'async_session' dependency.


async def on_startup(app: Litestar) -> None:
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


@get("/", name="welcome")
async def welcome() -> Template:
    return Template(template_name="welcome.html.jinja")


@get("/search", name="search")
async def search() -> Template:
    return Template(template_name="search.html.jinja")


@get("/organizations", name="organizations")
async def organizations() -> Template:
    return Template(template_name="organizations.html.jinja")

@get("/admin", name="admin")
async def admin() -> Template:
    return Template(template_name="admin.html.jinja")


def duration_format(value: float) -> str:
    hours = int(value // 3600)
    minutes = int((value % 3600) // 60)
    secs = int(value % 60)
    if hours > 0:
        return f"{hours}h{minutes}m{secs}s"
    else:
        return f"{minutes}m{secs}s"


env = Environment(loader=PackageLoader("app"), autoescape=select_autoescape())
env.filters["duration_format"] = duration_format

app = Litestar(
    route_handlers=[
        welcome,
        search,
        organizations,
        admin,
        CollectionController,
        PageController,
        ResourceController,
        create_static_files_router(path="/static", directories=["public"]),
    ],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine.from_environment(env),
    ),
    on_startup=[on_startup],
    plugins=[SQLAlchemyPlugin(config=sqlalchemy_config)],
    debug=True,
)
