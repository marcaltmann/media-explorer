from datetime import date
from pathlib import Path

from litestar import Litestar, get
from litestar.connection import Request
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.plugins.sqlalchemy import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyPlugin, base
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig
from sqlalchemy import ForeignKey, func, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship


from controllers.page_controller import PageController


ASSETS_DIR = Path("assets")


# The SQLAlchemy base includes a declarative model for you to use in your models.
class Resource(base.BigIntAuditBase):
    __tablename__ = "resource"
    name: Mapped[str]

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///test.sqlite", session_config=session_config, create_all=True
)  # Create 'async_session' dependency.

async def on_startup(app: Litestar) -> None:
    """Adds some dummy data if no data is present."""
    async with sqlalchemy_config.get_session() as session:
        statement = select(func.count()).select_from(Resource)
        count = await session.execute(statement)
        if not count.scalar():
            session.add(Resource(name="Stephen King"))
            session.add(Resource(name="Tony Blair"))
            await session.commit()



@get("/", name="welcome")
async def index() -> Template:
    title = "Media Explorer"
    return Template(template_name="welcome.html.jinja", context={"title": title})

@get("/collections", name="collections")
async def collections() -> Template:
    return Template(template_name="collections.html.jinja")

@get("/resources", name="resources")
async def resources(db_session: AsyncSession, db_engine: AsyncEngine) -> Template:
    resources = list(await db_session.scalars(select(Resource)))
    return Template(template_name="resources.html.jinja", context={"resources": resources})

@get("/resources/{resource_id:int}", name="resource-detail")
async def resource_detail(db_session: AsyncSession, resource_id: int) -> Template:
    resource = await db_session.get(Resource, resource_id)
    return Template(template_name="resource_detail.html.jinja", context={"resource": resource})

@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


app = Litestar(
    route_handlers=[
        index,
        collections,
        resources,
        resource_detail,
        get_book,
        PageController,
        create_static_files_router(path="/static", directories=["assets"]),
    ],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
    on_startup=[on_startup],
    plugins=[SQLAlchemyPlugin(config=sqlalchemy_config)],
    debug=True,
)
