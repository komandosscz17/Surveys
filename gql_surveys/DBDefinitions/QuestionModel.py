
import sqlalchemy


from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    
)

from sqlalchemy.orm import relationship

from .BaseModel import BaseModel
from .UUID import uuid
from.UUID import (UUIDFKey, UUIDColumn,)

class QuestionModel(BaseModel):
    __tablename__ = "surveyquestions"

    id = UUIDColumn()
    name = Column(String)  # kompletní znění otázky
    name_en = Column(String)
    order = Column(Integer)
    survey_id = Column(ForeignKey("surveys.id"), index=True)
    type_id = Column(ForeignKey("surveyquestiontypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
