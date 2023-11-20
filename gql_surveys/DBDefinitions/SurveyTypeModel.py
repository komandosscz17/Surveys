
import sqlalchemy


from sqlalchemy import (
    Column,
    String,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship

from .BaseModel import BaseModel
from .UUID import uuid
from.UUID import (UUIDFKey, UUIDColumn,)




class SurveyTypeModel(BaseModel):
    __tablename__ = "surveytypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

