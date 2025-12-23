from pathlib import Path

from advanced_alchemy.extensions.litestar import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)
from jinja2 import Environment, PackageLoader, select_autoescape
from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.datastructures import ResponseHeader
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig
from litestar_vite import ViteConfig, VitePlugin

from explorer.controllers import (
    AdminCategoryController,
    AdminCollectionController,
    AdminResourceController,
)
from explorer.controllers.welcome import WelcomeController
from explorer.controllers.page import PageController
from explorer.controllers.collection import CollectionController
from explorer.controllers.resource import ResourceController
from explorer.controllers.search import SearchController
from explorer.controllers.admin import AdminController
from explorer.controllers.organization import OrganizationController
from explorer.controllers.api import ApiController
from explorer.seeds.seed_db import seed_database
from explorer.utils.filters import duration_format
from explorer.config import Settings
from explorer.http import get_csp_header_value

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
    print('Byebye')


env = Environment(loader=PackageLoader('explorer'), autoescape=select_autoescape())
env.filters['duration_format'] = duration_format

vite = VitePlugin(config=ViteConfig())

app = Litestar(
    route_handlers=[
        WelcomeController,
        AdminController,
        AdminCategoryController,
        AdminCollectionController,
        AdminResourceController,
        OrganizationController,
        SearchController,
        CollectionController,
        PageController,
        ResourceController,
        ApiController,
        create_static_files_router(path='/', directories=['assets']),
        create_static_files_router(path='/media', directories=['media']),
    ],
    template_config=TemplateConfig(
        directory=Path('explorer/templates'),
        engine=JinjaTemplateEngine.from_environment(env),
    ),
    response_headers=[
        ResponseHeader(
            name='Content-Security-Policy',
            value=get_csp_header_value(settings.s3.S3_ENDPOINT_URL),
            description='Basic CSP rules',
        )
    ],
    on_startup=[on_startup],
    on_shutdown=[print_message],
    plugins=[vite, SQLAlchemyPlugin(config=sqlalchemy_config)],
    debug=True,
)
