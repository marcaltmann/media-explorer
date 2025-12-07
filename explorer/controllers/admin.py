from litestar import get
from litestar.controller import Controller
from litestar.response import Template
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from explorer.models import Collection, Resource


class AdminController(Controller):
    path = "/admin"

    @get("", name="admin")
    async def admin(self, db_session: AsyncSession) -> Template:
        statement = select(func.count("*")).select_from(Collection)
        result = await db_session.execute(statement)
        collection_count = result.scalar()

        statement = select(func.count("*")).select_from(Resource)
        result = await db_session.execute(statement)
        resource_count = result.scalar()

        await db_session.commit()

        return Template(
            template_name="admin/dashboard.html.jinja",
            context={
                "collection_count": collection_count,
                "resource_count": resource_count,
            },
        )
