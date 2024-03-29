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
    value = Column(String, comment="value of answer")
    aswered = Column(Boolean, comment="is answered")
    expired = Column(Boolean, comment = "is expired")
    user_id = UUIDFKey()#Column(ForeignKey("users.id"), index=True)
    question_id = Column(ForeignKey("surveyquestions.id"), primary_key=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(),  comment="Timestamp when the financial information category was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the financial information category")
    created_by = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changed_by = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
