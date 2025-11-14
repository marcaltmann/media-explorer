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
    return Template(template_name="welcome.html.jinja", context={"title": title})


@get("/contact", name="contact")
async def contact() -> Template:
    return Template(template_name="contact.html.jinja")

@get("/privacy", name="privacy")
async def privacy() -> Template:
    return Template(template_name="privacy.html.jinja")

@get("/accessibility", name="accessibility")
async def accessibility() -> Template:
    return Template(template_name="accessibility.html.jinja")

@get("/terms-of-use", name="terms-of-use")
async def terms_of_use() -> Template:
    return Template(template_name="terms_of_use.html.jinja")

@get("/legal-notice", name="legal-notice")
async def legal_notice() -> Template:
    return Template(template_name="legal_notice.html.jinja")




@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


app = Litestar(
    route_handlers=[
        index,
        contact,
        privacy,
        accessibility,
        terms_of_use,
        legal_notice,
        get_book,
        create_static_files_router(path="/static", directories=["assets"]),
    ],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
    on_startup=[on_startup],
)
