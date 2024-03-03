
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
    name = Column(String, comment= "name of survey type")
    name_en = Column(String, comment = "english name of survey type")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(),   comment="Timestamp when the financial information category was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the financial information category")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

