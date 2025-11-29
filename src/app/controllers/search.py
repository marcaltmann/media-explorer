from litestar import get
from litestar.controller import Controller
from litestar.response import Template


class SearchController(Controller):
    path = "/search"

    @get("", name="search")
    async def search(self) -> Template:
        return Template(template_name="search.html.jinja")
