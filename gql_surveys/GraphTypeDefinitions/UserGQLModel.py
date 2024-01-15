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
    resolve_authorization_id,
    resolve_user_id,
    resolve_accesslevel,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    createRootResolver_by_page,
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
        rows = await loader.filter_by(user_id = self.id)
        result = list(rows)
        print (result)
        return result
            # resolveAnswersForUser(session, self.id
            #                       )  
            # return result

    # @strawberryA.field(description="Assign survey to the user")
    # async def assignSurvey(
    #     self, info: strawberryA.types.Info, survey_id: uuid.UUID
    # ) -> typing.List["AnswerGQLModel"]:
    #     loader = getLoaders(info).surveys
    #     rows = await loader.filter_by(survey_id = self.id)
    #     result = list(rows)
    #     print (result)
    #     return result
        # async with withInfo(info) as session:
        #     # Implement logic for assigning survey to the user here
        #     result = await resolveAnswersForUser(session, self.id, survey_id)
        #     return result
#############################################################
#
# Queries
#
#############################################################
