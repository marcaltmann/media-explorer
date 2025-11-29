from typing import Optional

from litestar.plugins.sqlalchemy import base
from sqlalchemy import ForeignKey, func, select, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Collection(base.BigIntAuditBase):
    __tablename__ = "collection"
    name: Mapped[str]
    description: Mapped[str] = mapped_column(default="", nullable=False)
    color: Mapped[str] = mapped_column(default="#333", nullable=False)
    resources: Mapped[list[Resource]] = relationship(
        back_populates="collection", lazy="selectin"
    )

    def __repr__(self):
        return f"Collection(id={self.id}, name={self.name})"


class Resource(base.BigIntAuditBase):
    __tablename__ = "resource"
    name: Mapped[str]
    media_type: Mapped[str]
    url: Mapped[str]
    poster_url: Mapped[str] = mapped_column(default="")
    duration: Mapped[float]
    size: Mapped[Optional[int]] = mapped_column(default=0)
    toc: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    waveform: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    collection_id: Mapped[int] = mapped_column(ForeignKey("collection.id"))
    collection: Mapped[Collection] = relationship(
        lazy="joined", innerjoin=True, viewonly=True
    )

    def __repr__(self):
        return f"Resource(id={self.id}, name={self.name}, duration={self.duration})"

    def is_video(self):
        return self.media_type.startswith("video/")

    def is_audio(self):
        return self.media_type.startswith("audio/")
