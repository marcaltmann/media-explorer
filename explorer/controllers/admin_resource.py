from litestar import get, post
from litestar.controller import Controller
from litestar import Request
from litestar.datastructures import UploadFile
from litestar.response import Template, Redirect
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from explorer.config import Settings
from explorer.domain.resources.services import (
    probe_mediafile_metadata,
    format_to_media_type,
)
from explorer.models import Collection, Resource, MediaFile, License
from explorer.utils.s3 import store_fileobj
from explorer.use_cases.media_files import generate_derivatives

settings = Settings.from_env()


MAX_UPLOAD_SIZE = 1 * 1024**3  # 1GB


class AdminResourceController(Controller):
    path = '/admin/resources'

    @get('', name='admin-resource-list')
    async def admin_resource_list(self, db_session: AsyncSession) -> Template:
        statement = select(Resource).order_by(Resource.created_at.desc())
        result = await db_session.execute(statement)
        resources = result.scalars()

        statement = select(func.count('*')).select_from(Resource)
        result = await db_session.execute(statement)
        count = result.scalar()

        await db_session.commit()
        return Template(
            template_name='admin/resource_list.html.jinja',
            context={'resources': resources, 'count': count},
        )

    @get('/{resource_id:int}', name='admin-resource-detail')
    async def admin_resource_detail(
        self, db_session: AsyncSession, resource_id: int
    ) -> Template:
        resource = await db_session.get(Resource, resource_id)
        await db_session.commit()

        return Template(
            template_name='admin/resource_detail.html.jinja',
            context={'resource': resource},
        )

    @get('/new', name='admin-new-resource')
    async def admin_new_resource(self, db_session: AsyncSession) -> Template:
        statement = select(Collection).order_by(Collection.name.asc())
        result = await db_session.execute(statement)
        collection_list = result.scalars()
        await db_session.commit()

        return Template(
            template_name='admin/resource_new.html.jinja',
            context={'collection_list': collection_list, 'License': License},
        )

    @post('/new', name='admin-create-resource', request_max_body_size=MAX_UPLOAD_SIZE)
    async def admin_create_resource(
        self, db_session: AsyncSession, request: Request
    ) -> Redirect:
        form = await request.form()
        name: str = form.get('name')
        collection_id = int(form.get('collection_id'))

        file: UploadFile = form.get('file')
        url = store_fileobj(fileobj=file.file, filename=file.filename)

        data = probe_mediafile_metadata(url)
        duration = float(data['format']['duration'])
        format = data['format']['format_name']
        size = int(data['format']['size'])
        media_type = format_to_media_type(format)

        resource = Resource(
            name=name,
            collection_id=collection_id,
        )
        db_session.add(resource)
        await db_session.flush()

        media_file = MediaFile(
            filename=file.filename,
            type=media_type[0],
            sub_type=media_type[1],
            duration=duration,
            size=size,
            resource_id=resource.id,
        )
        db_session.add(media_file)
        await db_session.commit()

        # Thumbnails
        await generate_derivatives(media_file, db_session=db_session)

        return Redirect(path=f'/admin/resources/{resource.id}')
