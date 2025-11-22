from typing import Any

from litestar import get, MediaType
from litestar.controller import Controller
from litestar.response import Template
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from models import Resource


class ResourceController(Controller):
    path = "/resources"

    @get("", name="resources")
    async def resources(self, db_session: AsyncSession, db_engine: AsyncEngine) -> Template:
        resources = await db_session.scalars(select(Resource))
        return Template(
            template_name="resources.html.jinja", context={"resources": resources}
        )

    @get("/{resource_id:int}", name="resource-detail")
    async def resource_detail(self, db_session: AsyncSession, resource_id: int) -> Template:
        resource = await db_session.get(Resource, resource_id)
        return Template(
            template_name="resource_detail.html.jinja", context={"resource": resource}
        )

    @get("/{resource_id:int}/toc", name="resource-toc", media_type=MediaType.JSON)
    async def resource_toc(self, db_session: AsyncSession, resource_id: int) -> dict[str, Any]:
        resource = await db_session.get(Resource, resource_id)
        return resource.toc
