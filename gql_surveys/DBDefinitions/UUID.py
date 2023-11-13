from email.policy import default
import sqlalchemy


from sqlalchemy import (
    Column,
    String,
   
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base


import uuid

def newUuidAsString():
    return f"{uuid.uuid1()}"


def UUIDColumn(name=None):
    if name is None:
        return Column(String, primary_key=True, unique=True, default=newUuidAsString)
    else:
        return Column(
            name, String, primary_key=True, unique=True, default=newUuidAsString
        )

def CreateUUIDFKey(allowCross=False):
    def UUIDFKey(ForeignKey=None, *, nullable=False, index=True):
        assert ForeignKey is not None, "ForeignKey is mandatory"
        return Column(
            ForeignKey, index=index, nullable=nullable
        )
    
    def UUIDFKeyDummy(ForeignKey=None, *, nullable=False, index=True):
        return Column(
            String, index=index, nullable=nullable
        )
    
    if allowCross:
        return UUIDFKey
    else:
        return UUIDFKeyDummy
    
UUIDFKey = CreateUUIDFKey()

