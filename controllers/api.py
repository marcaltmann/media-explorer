from typing import Any, List

from litestar import get, delete, MediaType
from litestar.controller import Controller
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from models import Resource


class ApiController(Controller):
    path = "/api"

    @get("/resources", name="api-resources")
    async def resources(self, db_session: AsyncSession) -> List[Resource]:
        resources = await db_session.scalars(select(Resource))
        return list(resources)
