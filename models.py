from typing import Optional

from litestar.plugins.sqlalchemy import base
from sqlalchemy import ForeignKey, func, select, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Collection(base.BigIntAuditBase):
    __tablename__ = "collection"
    name: Mapped[str]
    description: Mapped[str] = mapped_column(default="", nullable=False)
    resources: Mapped[list[Resource]] = relationship(
        back_populates="collection", lazy="selectin"
    )

    def __repr__(self):
        return f"Collection(name={self.name})"


class Resource(base.BigIntAuditBase):
    __tablename__ = "resource"
    name: Mapped[str]
    media_type: Mapped[str]
    url: Mapped[str]
    poster_url: Mapped[str]
    duration: Mapped[float]
    toc: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    collection_id: Mapped[int] = mapped_column(ForeignKey("collection.id"))
    collection: Mapped[Collection] = relationship(
        lazy="joined", innerjoin=True, viewonly=True
    )

    def __repr__(self):
        return f"Resource(name={self.name})"

    def is_video(self):
        return self.media_type.startswith("video/")

    def is_audio(self):
        return self.media_type.startswith("audio/")
