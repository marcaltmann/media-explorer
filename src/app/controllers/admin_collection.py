from litestar import get, post
from litestar.controller import Controller
from litestar import Request
from litestar.response import Template, Redirect
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


class AdminCollectionController(Controller):
    path = "/admin/collections"

    @get("/new", name="admin-new-collection")
    async def admin_new_collection(self, db_session: AsyncSession) -> Template:
        return Template(
            template_name="admin/collection_new.html.jinja",
        )
