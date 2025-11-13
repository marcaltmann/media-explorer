from pathlib import Path

from litestar import Litestar, get
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig


ASSETS_DIR = Path("assets")


def on_startup():
    ASSETS_DIR.mkdir(exist_ok=True)


@get("/", name="welcome")
async def index() -> Template:
    title = "Media Explorer"
    return Template(template_name="welcome.html.jinja2", context={"title": title})


@get("/contact", name="contact")
async def contact() -> Template:
    return Template(template_name="contact.html.jinja2")

@get("/privacy", name="privacy")
async def privacy() -> Template:
    return Template(template_name="privacy.html.jinja2")

@get("/accessibility", name="accessibility")
async def accessibility() -> Template:
    return Template(template_name="accessibility.html.jinja2")



@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


app = Litestar(
    route_handlers=[
        index,
        contact,
        privacy,
        accessibility,
        get_book,
        create_static_files_router(path="/static", directories=["assets"]),
    ],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
    on_startup=[on_startup],
)
