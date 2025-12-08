from litestar import get
from litestar.controller import Controller
from litestar.response import Template


class OrganizationController(Controller):
    path = '/organizations'

    @get('', name='organizations')
    async def organizations(self) -> Template:
        return Template(template_name='organizations.html.jinja')
