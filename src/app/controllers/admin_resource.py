from litestar import get, post
from litestar.controller import Controller
from litestar import Request
from litestar.response import Template, Redirect
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models import Collection, Resource
from src.app.domain.resources.services import probe_mediafile_metadata, format_to_media_type


class AdminResourceController(Controller):
    path = "/admin/resources"

    @get("", name="admin-resource-list")
    async def resources(self, db_session: AsyncSession ) -> Template:
        statement = select(Resource).order_by(Resource.created_at.desc())
        result = await db_session.execute(statement)
        resources = result.scalars()

        statement = select(func.count("*")).select_from(Resource)
        result = await db_session.execute(statement)
        count = result.scalar()

        await db_session.commit()
        return Template(
            template_name="admin/resource_list.html.jinja", context={"resources": resources, "count": count}
        )

    @get("/new", name="admin-new-resource")
    async def new_resource(self, db_session: AsyncSession) -> Template:
        statement = select(Collection).order_by(Collection.name.asc())
        result = await db_session.execute(statement)
        collection_list = result.scalars()
        await db_session.commit()

        return Template(
            template_name="admin/resource_new.html.jinja",
            context={"collection_list": collection_list},
        )

    @post("/new", name="admin-create-resource")
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
