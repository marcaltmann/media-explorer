from dataclasses import dataclass
from pathlib import Path

from litestar import Litestar, get
from litestar.connection import Request
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig

from controllers.page_controller import PageController


ASSETS_DIR = Path("assets")


@dataclass
class Resource:
    id: int
    name: str


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
    resources = [
        Resource(id=1, name="Interview Phil Collins"),
        Resource(id=2, name="Interview David Bowie"),
    ]
    return Template(template_name="resources.html.jinja", context={"resources": resources})

@get("/resources/{resource_id:int}", name="resource-detail")
async def resource_detail(resource_id: int) -> Template:
    resources = {
        1: Resource(id=1, name="Interview Phil Collins"),
        2: Resource(id=2, name="Interview David Bowie"),
    }
    resource = resources[resource_id]
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
)
