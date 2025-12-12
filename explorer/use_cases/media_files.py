from sqlalchemy.ext.asyncio import AsyncSession

from explorer.models import MediaFile, DerivativeFile, DerivativeType
from explorer.utils.ffmpeg import create_thumbnail


async def create_derivatives(
    media_file: MediaFile, db_session: AsyncSession, s3_client
) -> None:
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

    """
    Steps:
    Check if media file has url, otherwise fail.
    Call ffmpeg function which returns? Maybe temporary file.
    Save temporary file with s3.
    Create a new Derivative file in the database.
    """

    assert media_file.url is not None

    lg = create_thumbnail(media_file.url, 480)
    md = create_thumbnail(media_file.url, 320)
    sm = create_thumbnail(media_file.url, 160)

    # s3 stuff -> maybe do not do it directly.

    large_file = DerivativeFile(
        type=DerivativeType.thumbnail_480,
        media_type='image/webp',
        media_file=media_file,
    )
    medium_file = DerivativeFile(
        type=DerivativeType.thumbnail_320,
        media_type='image/webp',
        media_file=media_file,
    )
    small_file = DerivativeFile(
        type=DerivativeType.thumbnail_160,
        media_type='image/webp',
        media_file=media_file,
    )
    db_session.add_all([large_file, medium_file, small_file])
    await db_session.commit()
