
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
    name = Column(String, comment = "Name of question")
    name_en = Column(String, comment= "english name of question")
    order = Column(Integer, comment = "order of questions")
    survey_id = UUIDFKey()#Column(ForeignKey("surveys.id"), index=True)
    type_id = Column(ForeignKey("surveyquestiontypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(),  comment="Timestamp when the financial information category was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the financial information category")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
