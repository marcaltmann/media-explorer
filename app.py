from datetime import date
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape
from litestar import Litestar, get
from litestar.connection import Request
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin
)
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig
from sqlalchemy import ForeignKey, func, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


from controllers.page_controller import PageController

from models import Resource
from seeds import get_resources


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
            session.add_all(get_resources())
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
