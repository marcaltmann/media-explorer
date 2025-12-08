from litestar import get
from litestar.controller import Controller
from litestar.response import Template
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from explorer.models import Collection


class CollectionController(Controller):
    path = '/collections'

    @get('', name='collections')
    async def collections(
        self, db_session: AsyncSession, db_engine: AsyncEngine
    ) -> Template:
        collections = await db_session.scalars(select(Collection))
        await db_session.commit()

        return Template(
            template_name='collections.html.jinja', context={'collections': collections}
        )

    @get('/{collection_id:int}', name='collection-detail')
    async def collection_detail(
        self, db_session: AsyncSession, db_engine: AsyncEngine, collection_id: int
    ) -> Template:
        collection = await db_session.get(Collection, collection_id)
        await db_session.commit()
        return Template(
            template_name='collection_detail.html.jinja',
            context={'collection': collection},
        )
