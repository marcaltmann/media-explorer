from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape
from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig

from controllers.welcome import WelcomeController
from controllers.page import PageController
from controllers.collection import CollectionController
from controllers.resource import ResourceController
from controllers.search import SearchController
from controllers.admin import AdminController
from controllers.organization import OrganizationController

from seeds.seed_db import seed_database
from utils.filters import duration_format

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///test.sqlite",
    session_config=session_config,
    create_all=True,
)


async def on_startup(app: Litestar) -> None:
    await seed_database(sqlalchemy_config)


env = Environment(loader=PackageLoader("app"), autoescape=select_autoescape())
env.filters["duration_format"] = duration_format

app = Litestar(
    route_handlers=[
        WelcomeController,
        AdminController,
        OrganizationController,
        SearchController,
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
