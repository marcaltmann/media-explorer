from pathlib import Path

from litestar import Litestar, get
from litestar.connection import Request
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig

from controllers.page_controller import PageController


ASSETS_DIR = Path("assets")


def on_startup():
    ASSETS_DIR.mkdir(exist_ok=True)


@get("/", name="welcome")
async def index() -> Template:
    title = "Media Explorer"
    return Template(template_name="welcome.html.jinja", context={"title": title})

@get("/collections", name="collections")
async def collections() -> Template:
    return Template(template_name="collections.html.jinja")

@get("/resources", name="resources")
async def resources() -> Template:
    return Template(template_name="resources.html.jinja")

@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


app = Litestar(
    route_handlers=[
        index,
        collections,
        resources,
        get_book,
        PageController,
        create_static_files_router(path="/static", directories=["assets"]),
    ],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
    on_startup=[on_startup],
)
