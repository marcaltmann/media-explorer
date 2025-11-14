from litestar import get
from litestar.controller import Controller
from litestar.response import Template


class PageController(Controller):
    path = "/pages"

    @get("/contact", name="contact")
    async def contact(self) -> Template:
        return Template(template_name="contact.html.jinja")

    @get("/privacy", name="privacy")
    async def privacy(self) -> Template:
        return Template(template_name="privacy.html.jinja")

    @get("/accessibility", name="accessibility")
    async def accessibility(self) -> Template:
        return Template(template_name="accessibility.html.jinja")

    @get("/terms-of-use", name="terms-of-use")
    async def terms_of_use(self) -> Template:
        return Template(template_name="terms_of_use.html.jinja")

    @get("/legal-notice", name="legal-notice")
    async def legal_notice(self) -> Template:
        return Template(template_name="legal_notice.html.jinja")
