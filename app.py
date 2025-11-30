from os import getenv
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
from litestar_vite import ViteConfig, VitePlugin

from src.app.controllers.welcome import WelcomeController
from src.app.controllers.page import PageController
from src.app.controllers.collection import CollectionController
from src.app.controllers.resource import ResourceController
from src.app.controllers.search import SearchController
from src.app.controllers.admin import AdminController
from src.app.controllers.admin_collection import AdminCollectionController
from src.app.controllers.admin_resource import AdminResourceController
from src.app.controllers.organization import OrganizationController
from src.app.controllers.api import ApiController

from src.seeds.seed_db import seed_database
from src.utils.filters import duration_format

from src.app.config import Settings

settings = Settings.from_env()


session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=settings.db.URL,
    session_config=session_config,
    create_all=True,
)

async def on_startup(app: Litestar) -> None:
    await seed_database(sqlalchemy_config)


def print_message() -> None:
    print("Byebye")


env = Environment(loader=PackageLoader("app"), autoescape=select_autoescape())
env.filters["duration_format"] = duration_format

vite = VitePlugin(config=ViteConfig())

app = Litestar(
    route_handlers=[
        WelcomeController,
        AdminController,
        AdminCollectionController,
        AdminResourceController,
        OrganizationController,
        SearchController,
        CollectionController,
        PageController,
        ResourceController,
        ApiController,
        create_static_files_router(path="/", directories=["assets"]),
        create_static_files_router(path="/media", directories=["media"]),
    ],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine.from_environment(env),
    ),
    on_startup=[on_startup],
    on_shutdown=[print_message],
    plugins=[vite, SQLAlchemyPlugin(config=sqlalchemy_config)],
    debug=True,
)
