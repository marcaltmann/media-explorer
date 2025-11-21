from pathlib import Path

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

from controllers.page_controller import PageController
from controllers.collection_controller import CollectionController
from controllers.resource_controller import ResourceController
from seeds.seed_db import seed_database
from utils.filters import duration_format

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///test.sqlite",
    session_config=session_config,
    create_all=True,
)  # Create 'async_session' dependency.


async def on_startup(app: Litestar) -> None:
    await seed_database(sqlalchemy_config)


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
