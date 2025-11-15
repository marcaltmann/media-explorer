from litestar.plugins.sqlalchemy import base
from sqlalchemy.orm import Mapped, mapped_column, relationship


# The SQLAlchemy base includes a declarative model for you to use in your models.
class Resource(base.BigIntAuditBase):
    __tablename__ = "resource"
    name: Mapped[str]
    media_type: Mapped[str]
    url: Mapped[str]
    poster_url: Mapped[str]
    duration: Mapped[float]

    def __repr__(self):
        return f"Resource(name={self.name})"
