from email.policy import default
import sqlalchemy


from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,

)


from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

from .BaseModel import BaseModel
from .UUID import uuid
from.UUID import (UUIDFKey, UUIDColumn,)

# id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

class QuestionValueModel(BaseModel):
    __tablename__ = "surveyquestionvalues"

    id = UUIDColumn()
    name = Column(String, comment = "name of questionvalue") 
    name_en = Column(String, comment = "name of questionvalue in english")
    order = Column(Integer, comment = "order of queationvalues")
    question_id = Column(ForeignKey("surveyquestions.id"), index=True)
    
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the financial information category was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the financial information category")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
