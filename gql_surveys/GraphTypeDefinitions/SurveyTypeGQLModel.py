from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
import datetime
from .BaseGQLModel import BaseGQLModel



        
@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a group""",
)
class SurveyTypeGQLModel(BaseGQLModel):
    

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Survey name""")
    def name(self) -> str:
        return self.name
#############################################################
#
# Queries
#
#############################################################

