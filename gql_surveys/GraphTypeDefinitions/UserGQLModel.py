from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager
import datetime
from typing import Annotated
from .BaseGQLModel import BaseGQLModel
from .GraphResolvers import (
    resolveSurveyById,
    resolveQuestionById,
    resolveAnswerById,
    resolveQuestionTypeById,
    resolveAnswersForQuestion,
    resolveAnswersForUser,
    resolveQuestionForSurvey,
)
@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass
        

AnswerGQLModel = Annotated["AnswerGQLModel", strawberryA.lazy(".AnswerGQLModel")]
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)
    
    

  
    @strawberryA.field(description="""List""")
    async def answers(
        self, info: strawberryA.types.Info
    ) -> typing.List["AnswerGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveAnswersForUser(session, self.id)
            return result

    @strawberryA.field(description="""Lisooot""")
    async def assignSurvey(
        self, info: strawberryA.types.Info, survey_id: strawberryA.ID
    ) -> typing.List["AnswerGQLModel"]:  ###############
        async with withInfo(info) as session:
            result = await resolveAnswersForUser(session, self.id)
            return result
#############################################################
#
# Queries
#
#############################################################
