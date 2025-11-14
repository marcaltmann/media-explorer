from datetime import date
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape
from litestar import Litestar, get
from litestar.connection import Request
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
    base,
)
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig
from sqlalchemy import ForeignKey, func, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship


from controllers.page_controller import PageController


# The SQLAlchemy base includes a declarative model for you to use in your models.
class Resource(base.BigIntAuditBase):
    __tablename__ = "resource"
    name: Mapped[str]
    media_type: Mapped[str]
    url: Mapped[str]
    poster_url: Mapped[str]
    duration: Mapped[float]


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
            session.add_all([
                Resource(
                    name="Again to the Front (1952)",
                    media_type="video/webm",
                    url="https://upload.wikimedia.org/wikipedia/commons/f/f3/Again_to_the_Front_%281952%29_%E2%80%93_Mandarin_Chinese_dub.webm",
                    poster_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Again_to_the_Front_%281952%29_%E2%80%93_Mandarin_Chinese_dub.webm/639px--Again_to_the_Front_%281952%29_%E2%80%93_Mandarin_Chinese_dub.webm.jpg?20240730091952",
                    duration=4603.144,
                ),
                Resource(
                    name="Trump Welcomes Citizens",
                    media_type="video/webm",
                    url="https://upload.wikimedia.org/wikipedia/commons/transcoded/7/74/PRESIDENT_DONALD_J._TRUMP_WELCOMES_AMERICA%E2%80%99S_NEWEST_CITIZENS_%F0%9F%87%BA%F0%9F%87%B8%F0%9F%A6%85.webm/PRESIDENT_DONALD_J._TRUMP_WELCOMES_AMERICA%E2%80%99S_NEWEST_CITIZENS_%F0%9F%87%BA%F0%9F%87%B8%F0%9F%A6%85.webm.1080p.vp9.webm",
                    poster_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/PRESIDENT_DONALD_J._TRUMP_WELCOMES_AMERICA%E2%80%99S_NEWEST_CITIZENS_%F0%9F%87%BA%F0%9F%87%B8%F0%9F%A6%85.webm/800px--PRESIDENT_DONALD_J._TRUMP_WELCOMES_AMERICA%E2%80%99S_NEWEST_CITIZENS_%F0%9F%87%BA%F0%9F%87%B8%F0%9F%A6%85.webm.jpg",
                    duration=103.908,
                ),
                Resource(
                    name="Chinese Cuisine of Fried Rice",
                    media_type="video/webm",
                    url="https://upload.wikimedia.org/wikipedia/commons/e/eb/Chinese_cuisine_of_Fried_Rice.webm",
                    poster_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Chinese_cuisine_of_Fried_Rice.webm/640px--Chinese_cuisine_of_Fried_Rice.webm.jpg?20130912140344",
                    duration=187.649,
                ),
            ])
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


@get("/collections", name="collections")
async def collections() -> Template:
    return Template(template_name="collections.html.jinja")


@get("/resources", name="resources")
async def resources(db_session: AsyncSession, db_engine: AsyncEngine) -> Template:
    resources = list(await db_session.scalars(select(Resource)))
    return Template(
        template_name="resources.html.jinja", context={"resources": resources}
    )


@get("/resources/{resource_id:int}", name="resource-detail")
async def resource_detail(db_session: AsyncSession, resource_id: int) -> Template:
    resource = await db_session.get(Resource, resource_id)
    return Template(
        template_name="resource_detail.html.jinja", context={"resource": resource}
    )


@get("/admin", name="admin")
async def admin() -> Template:
    return Template(template_name="admin.html.jinja")


def duration_format(value: float) -> str:
    hours = int(value // 3600)
    minutes = int((value % 3600) // 60)
    secs = int(value % 60)
    return f"{hours}h{minutes}m{secs}s"

env = Environment(
    loader=PackageLoader("app"),
    autoescape=select_autoescape()
)
env.filters["duration_format"] = duration_format

app = Litestar(
    route_handlers=[
        welcome,
        search,
        organizations,
        collections,
        resources,
        resource_detail,
        admin,
        PageController,
        create_static_files_router(path="/static", directories=["assets"]),
    ],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine.from_environment(env),
    ),
    on_startup=[on_startup],
    plugins=[SQLAlchemyPlugin(config=sqlalchemy_config)],
    debug=True,
)
