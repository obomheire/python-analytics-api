import uuid
from datetime import datetime, timezone
from typing import List, Optional
import sqlmodel
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID  # only needed for PostgreSQL
from sqlmodel import Field, SQLModel


def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


class StrictBaseModel(BaseModel):
    class Config:
        extra = "forbid"  # Dont allow extra fields


class EventModel(SQLModel, table=True):
    __tablename__ = "event_model"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        sa_type=UUID(as_uuid=True),
        sa_column_kwargs={"server_default": None},
    )
    page: str = Field(index=True)
    description: Optional[str] = Field(default="")
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False,
    )


class EventCreateSchema(StrictBaseModel):
    page: str
    description: Optional[str] = ""


class EventUpdateSchema(SQLModel):
    page: Optional[str] = None
    description: Optional[str] = None


# {"id": 12}


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int
