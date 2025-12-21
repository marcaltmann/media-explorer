"""Use cases for resources"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from explorer.models import Resource


# Use case input/output DTOs
@dataclass
class CreateResourceRequest:
    name: str
    description: str


@dataclass
class CreateResourceResponse:
    resource: Resource
    success: bool
    error: Optional[str] = None


class CreateResourceUseCase:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def execute(self, request: CreateResourceRequest) -> CreateResourceResponse:
        # Validation

        # Business logic

        # Create and save
        resource = Resource(
            name=request.name,
            description=request.description,
        )
        self.db_session.add(resource)
        await self.db_session.commit()

        return CreateResourceResponse(resource=resource, success=True)


# Also, delete resource use case:
#
# - Delete poster image's stored files
# - Delete poster image from db
# - Delete media files' stored files
# - Delete resource
#
# This is why generic active storage like db could be handy.
# As soon as db entry is deleted, storage is deleted.
