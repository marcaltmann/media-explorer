import os

from sqlalchemy.ext.asyncio import AsyncSession

from explorer.models import MediaFile, DerivativeFile, DerivativeType
from explorer.utils.ffmpeg import generate_thumbnail
from explorer.utils.s3 import store_file


async def generate_derivatives(media_file: MediaFile, db_session: AsyncSession) -> None:
    """
    Use case function for creating all the derivative files from
    a media file that has already been persisted, i.e. for which
    we already have a URL.
    This is a draft version. Could also be a class in the future.
    We also could add dependency injection for e.g.:
    - S3 client
    - Database repository

    Also, this thing should be started as a background task or
    something. Or it should start background tasks. I don't
    know.
    Poster images/thumbnails should be separate because thumbnails
    do not need to wait for the video derivatives.
    """

    url = media_file.get_url()

    # Check if media file has url, otherwise fail.
    # This does not have any effect, there is no way to check if
    # the media file has been persisted yet.
    assert url is not None

    # Call ffmpeg function which returns temporary file path.
    path_lg = generate_thumbnail(url, width=480)
    path_md = generate_thumbnail(url, width=320)
    path_sm = generate_thumbnail(url, width=160)

    # Save temporary file with S3.
    store_file(path_lg, f'{media_file.uuid}/thumb-lg.webp')
    store_file(path_md, f'{media_file.uuid}/thumb-md.webp')
    store_file(path_sm, f'{media_file.uuid}/thumb-sm.webp')

    # Delete temporary files
    os.unlink(path_lg)
    os.unlink(path_md)
    os.unlink(path_sm)

    # Create a new Derivative file in the database.
    # This is kind of stupid.
    large_file = DerivativeFile(
        type=DerivativeType.thumbnail_480,
        media_type='image/webp',
        media_file_id=media_file.id,
    )
    medium_file = DerivativeFile(
        type=DerivativeType.thumbnail_320,
        media_type='image/webp',
        media_file_id=media_file.id,
    )
    small_file = DerivativeFile(
        type=DerivativeType.thumbnail_160,
        media_type='image/webp',
        media_file_id=media_file.id,
    )
    db_session.add_all([large_file, medium_file, small_file])
    await db_session.commit()
