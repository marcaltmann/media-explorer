from litestar import get, post
from litestar.controller import Controller
from litestar import Request
from litestar.response import Template, Redirect
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from explorer.models import Category


class AdminCategoryController(Controller):
    path = '/admin/categories'

    @get('', name='admin-category-list')
    async def admin_category_list(self, db_session: AsyncSession) -> Template:
        statement = select(Category).order_by(Category.name.asc())
        result = await db_session.execute(statement)
        category_list = result.scalars()

        statement = select(func.count('*')).select_from(Category)
        result = await db_session.execute(statement)
        count = result.scalar()

        await db_session.commit()
        return Template(
            template_name='admin/category_list.html.jinja',
            context={'category_list': category_list, 'count': count},
        )

    @get('/{category_id:int}', name='admin-category-detail')
    async def admin_category_detail(
        self, db_session: AsyncSession, category_id: int
    ) -> Template:
        category = await db_session.get(Category, category_id)
        await db_session.commit()
        return Template(
            template_name='admin/category_detail.html.jinja',
            context={'category': category},
        )

    @get('/new', name='admin-new-category')
    async def admin_new_category(self, db_session: AsyncSession) -> Template:
        return Template(
            template_name='admin/category_new.html.jinja',
        )

    @post('/new', name='admin-create-category')
    async def admin_create_category(
        self, db_session: AsyncSession, request: Request
    ) -> Redirect:
        form = await request.form()
        name = form.get('name')
        description = form.get('description')
        wikidata_id = form.get('wikidata_id')

        category = Category(
            name=name,
            description=description,
            wikidata_id=wikidata_id,
        )

        db_session.add(category)
        await db_session.commit()

        return Redirect(path=f'/admin/categories/{category.id}')
