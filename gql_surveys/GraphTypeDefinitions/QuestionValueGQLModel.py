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
    keys=["id"], description="""Entity representing an access to information"""
)
class QuestionValueGQLModel(BaseGQLModel):
    

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""Name aka, value of answer""")
    def name(self) -> Union[str, None]:
        return self.name
    
    @strawberryA.field(description="""English name aka, value of answer""")
    def name_en(self) -> Union[str, None]:
        return self.name_en

    @strawberryA.field(description="""order of value""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""Question which has this possible answer""")
    async def question(self, info: strawberryA.types.Info) -> Union[QuestionGQLModel, None]:
        result = await QuestionGQLModel.resolve_reference(info, self.question_id)
        return result
#############################################################
#
# Queries
#
#############################################################
