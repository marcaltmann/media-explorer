from dataclasses import dataclass
from typing import Annotated, Any
import msgspec


from litestar import Litestar, get, post, MediaType
from litestar.controller import Controller
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar import Request
from litestar.response import Template, Redirect
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from models import Resource


class ResourceController(Controller):
    path = "/resources"

    @get("", name="resources")
    async def resources(
        self, db_session: AsyncSession, db_engine: AsyncEngine
    ) -> Template:
        statement = select(Resource).order_by(Resource.media_type.desc())
        result = await db_session.execute(statement)
        resources = result.scalars()
        await db_session.commit()
        return Template(
            template_name="resources.html.jinja", context={"resources": resources}
        )

    @get("/{resource_id:int}", name="resource-detail")
    async def resource_detail(
        self, db_session: AsyncSession, resource_id: int
    ) -> Template:
        resource = await db_session.get(Resource, resource_id)
        await db_session.commit()

        return Template(
            template_name="resource_detail.html.jinja", context={"resource": resource}
        )

    @get("/new", name="resource-new")
    async def resource_new(self, db_session: AsyncSession) -> Template:
        return Template(template_name="resource_new.html.jinja")

    @post("/new", name="create-resource")
    async def create_resource(
        self, db_session: AsyncSession, request: Request
    ) -> Redirect:
        form = await request.form()
        name = form.get("name")

        resource = Resource(
            name=name,
            media_type="video/mp4",
            url="http://www.example.com",
            poster_url="http://www.example.com",
            duration=1000,
            collection_id=2
        )
        db_session.add(resource)
        await db_session.commit()

        return Redirect(path=f"/resources/{resource.id}")

    @get("/{resource_id:int}/toc", name="resource-toc", media_type=MediaType.JSON)
    async def resource_toc(
        self, db_session: AsyncSession, resource_id: int
    ) -> dict[str, Any]:
        resource = await db_session.get(Resource, resource_id)
        return resource.toc

    @get(
        "/{resource_id:int}/waveform",
        name="resource-waveform",
        media_type=MediaType.JSON,
    )
    async def resource_waveform(
        self, db_session: AsyncSession, resource_id: int
    ) -> dict[str, Any]:
        resource = await db_session.get(Resource, resource_id)
        return resource.waveform
