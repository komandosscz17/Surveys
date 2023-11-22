from typing import List, Union
import typing
import strawberry as strawberryA
from .extra import getLoaders, AsyncSessionFromInfo


import datetime
from contextlib import asynccontextmanager
from .GraphResolvers import (
    resolveSurveyById,
    resolveQuestionById,
    resolveAnswerById,
    resolveQuestionTypeById,
    resolveAnswersForQuestion,
    resolveAnswersForUser,
    resolveQuestionForSurvey,
)   
from typing import Annotated

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass
UserGQLModel = Annotated["UserGQLModel", strawberryA.lazy(".UserGQLModel")]
QuestionGQLModel = Annotated["QuestionGQLModel", strawberryA.lazy(".QuestionGQLModel")]
@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)
class AnswerGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).answers
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""answer content / value""")
    def value(self) -> Union[str, None]:
        return self.value

    @strawberryA.field(description="""is the survey already answered?""")
    async def aswered(self) -> Union[bool, None]:
        return self.aswered

    @strawberryA.field(description="""is the survey still available?""")
    async def expired(self) -> Union[bool, None]:
        return self.expired

    @strawberryA.field(
        description="""is the survey still available?"""
    )  # mimo náš kontejner
    async def user(self) -> UserGQLModel:
        return await UserGQLModel.resolve_reference(self.user_id)

    @strawberryA.field(
        description="""is the survey still available?"""
    )  # v našem kontejneru
    async def question(self, info: strawberryA.types.Info) -> QuestionGQLModel:
        return await QuestionGQLModel.resolve_reference(info, self.question_id)
#############################################################
#
# Queries
#
#############################################################
