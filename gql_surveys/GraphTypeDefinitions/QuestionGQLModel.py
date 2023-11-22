from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
from typing import Annotated
import datetime
from contextlib import asynccontextmanager
from .BaseGQLModel import BaseGQLModel

from .GraphResolvers import (
    resolveAnswersForQuestion,
)

def getLoader(info):
        return info.context['all']
@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

AnswerGQLModel = Annotated["AnswerGQLModel", strawberryA.lazy(".AnswerGQLModel")]
SurveyGQLModel = Annotated["SurveyGQLModel", strawberryA.lazy(".SurveyGQLModel")]
QuestionTypeGQLModel = Annotated["QuestionTypeGQLModel", strawberryA.lazy(".QuestionTypeGQLModel")]
QuestionValueGQLModel = Annotated["QuestionValueGQLModel", strawberryA.lazy(".QuestionValueGQLModel")]

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)
class QuestionGQLModel(BaseGQLModel):
    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""time stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Question""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Order of questions""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""List of answers related to the user""")
    async def answers(
        self, info: strawberryA.types.Info
    ) -> typing.List["AnswerGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveAnswersForQuestion(session, self.id)
            return result

    @strawberryA.field(description="""Survey which owns this question""")
    async def survey(
        self, info: strawberryA.types.Info
    ) -> typing.Union["SurveyGQLModel", None]:
        result = await SurveyGQLModel.resolve_reference(info, self.survey_id)
        return result

    @strawberryA.field(description="""Type of question""")
    async def type(
        self, info: strawberryA.types.Info
    ) -> typing.Union["QuestionTypeGQLModel", None]:
        result = await QuestionTypeGQLModel.resolve_reference(info, self.type_id)
        return result

    @strawberryA.field(description="""List of values for closed or similar type questions""")
    async def values(
        self, info: strawberryA.types.Info
    ) -> typing.List["QuestionValueGQLModel"]:
         
        loader = getLoader(info).questionvalues
        result = await loader.filter_by(question_id=self.id)
        return result
#############################################################
#
# Queries
#
#############################################################
