from litestar import get
from litestar.controller import Controller
from litestar.response import Template


class AdminController(Controller):
    path = "/admin"

    @get("", name="admin")
    async def admin(self) -> Template:
        return Template(template_name="admin.html.jinja")
