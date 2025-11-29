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

from src.app.models import Collection, Resource
from src.app.domain.resources.services import probe_mediafile_metadata, format_to_media_type


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

    @get("/new", name="new-resource")
    async def new_resource(self, db_session: AsyncSession) -> Template:
        statement = select(Collection).order_by(Collection.name.asc())
        result = await db_session.execute(statement)
        collection_list = result.scalars()
        await db_session.commit()

        return Template(
            template_name="resource_new.html.jinja",
            context={"collection_list": collection_list},
        )

    @post("/new", name="create-resource")
    async def create_resource(
        self, db_session: AsyncSession, request: Request
    ) -> Redirect:
        form = await request.form()
        name = form.get("name")
        url = form.get("url")
        collection_id = int(form.get("collection_id"))

        data = probe_mediafile_metadata(url)
        duration = float(data["format"]["duration"])
        format = data["format"]["format_name"]
        size = int(data["format"]["size"])
        media_type = format_to_media_type(format)

        resource = Resource(
            name=name,
            media_type=media_type,
            url=url,
            size=size,
            duration=duration,
            collection_id=collection_id,
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
