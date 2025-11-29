from litestar import get, post
from litestar.controller import Controller
from litestar import Request
from litestar.response import Template, Redirect
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models import Collection


class AdminCollectionController(Controller):
    path = "/admin/collections"

    @get("", name="admin-collection-list")
    async def admin_collection_list(self, db_session: AsyncSession) -> Template:
        statement = select(Collection).order_by(Collection.name.asc())
        result = await db_session.execute(statement)
        collection_list = result.scalars()

        statement = select(func.count("*")).select_from(Collection)
        result = await db_session.execute(statement)
        count = result.scalar()

        await db_session.commit()
        return Template(
            template_name="admin/collection_list.html.jinja",
            context={"collection_list": collection_list, "count": count},
        )

    @get("/{collection_id:int}", name="admin-collection-detail")
    async def admin_collection_detail(
        self, db_session: AsyncSession, collection_id: int
    ) -> Template:
        collection = await db_session.get(Collection, collection_id)
        await db_session.commit()
        return Template(
            template_name="admin/collection_detail.html.jinja",
            context={"collection": collection},
        )

    @get("/new", name="admin-new-collection")
    async def admin_new_collection(self, db_session: AsyncSession) -> Template:
        return Template(
            template_name="admin/collection_new.html.jinja",
        )

    @post("/new", name="admin-create-collection")
    async def admin_create_collection(
        self, db_session: AsyncSession, request: Request
    ) -> Redirect:
        form = await request.form()
        name = form.get("name")
        description = form.get("description")
        color = form.get("color")

        collection = Collection(
            name=name,
            description=description,
            color=color,
        )
        db_session.add(collection)
        await db_session.commit()

        return Redirect(path=f"/admin/collections/{collection.id}")
