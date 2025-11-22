from litestar import get
from litestar.controller import Controller
from litestar.response import Template


class WelcomeController(Controller):
    path = ""

    @get("/", name="welcome")
    async def welcome(self) -> Template:
        return Template(template_name="welcome.html.jinja")
