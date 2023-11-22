from typing import List, Union
import typing
import strawberry as strawberryA
from .BaseGQLModel import BaseGQLModel
from contextlib import asynccontextmanager
import datetime
from typing import Annotated

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
        


QuestionGQLModel = Annotated["QuestionGQLModel", strawberryA.lazy(".QuestionGQLModel")]
@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a group""",
)
class SurveyGQLModel(BaseGQLModel):
    

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Survey name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""List""")
    async def questions(
        self, info: strawberryA.types.Info
    ) -> typing.List["QuestionGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveQuestionForSurvey(session, self.id)
            return result


#     @strawberryA.field(description="""List""")
#     async def editor(self, info: strawberryA.types.Info) -> 'SurveyEditorGQLModel':
#         return self

# @strawberryA.federation.type(keys=["id"], description="""Editor""") ###############
# class SurveyEditorGQLModel:
#     pass

#############################################################
#
# Queries
#
#############################################################
