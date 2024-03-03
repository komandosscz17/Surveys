from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager
import datetime
from typing import Annotated
from .BaseGQLModel import BaseGQLModel
from gql_surveys.Dataloaders import getLoaders
from .GraphResolvers import (
    resolveAnswersForUser,
    resolve_id,
    resolve_name,
    resolve_name_en,    
    resolve_user_id,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
   
)
AnswerGQLModel = Annotated["AnswerGQLModel", strawberryA.lazy(".AnswerGQLModel")]

@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel(BaseGQLModel):
    id: uuid.UUID = strawberryA.federation.field(external=True)
    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return UserGQLModel(id=id)
    
    
    
    @strawberryA.field(description="List of answers for the user")
    async def answers(
        self, info: strawberryA.types.Info
    ) -> typing.List["AnswerGQLModel"]:
        loader = getLoaders(info).answers
        result = await loader.filter_by(user_id = self.id)
        return result
            # resolveAnswersForUser(session, self.id
            #                       )  
            # return result
