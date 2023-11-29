from email.policy import default
import sqlalchemy


from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

from .BaseModel import BaseModel
from.UUID import (UUIDFKey, UUIDColumn,)

# id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)



class AnswerModel(BaseModel):
    __tablename__ = "surveyanswers"

    id = UUIDColumn()
    value = Column(String)
    aswered = Column(Boolean)
    expired = Column(Boolean)
    user_id = UUIDFKey()#Column(ForeignKey("users.id"), index=True)
    question_id = Column(ForeignKey("surveyquestions.id"), primary_key=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
