from typing import List, Union
import typing
import strawberry as strawberryA
from .BaseGQLModel import BaseGQLModel
from contextlib import asynccontextmanager
import datetime
from typing import Annotated
from .extra import getLoaders

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
    @classmethod
    def getLoader(cls, info):
        return getLoaders(info).questionvalues

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

#############################################################
#
# Mutations
#
#############################################################

from typing import Optional
import datetime


@strawberryA.input
class QuestionValueInsertGQLModel:
    question_id: strawberryA.ID
    name: str
    name_en: Optional[str] = ""   
    order: Optional[int] = 1
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class QuestionValueUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    name: Optional[str] = None
    name_en: Optional[str] = None
    order: Optional[int] = None

@strawberryA.type
class QuestionValueResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of question operation""")
    async def question(self, info: strawberryA.types.Info) -> Union[QuestionValueGQLModel, None]:
        result = await QuestionValueGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.mutation(description="""Creates new question value for closed question""")
async def question_value_insert(self, info: strawberryA.types.Info, question_value: QuestionValueInsertGQLModel) -> QuestionValueResultGQLModel:
        loader = getLoaders(info).questionvalues
        row = await loader.insert(question_value)
        result = QuestionValueResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberryA.mutation(description="""Updates question value / possible answer""")
async def question_value_update(self, info: strawberryA.types.Info, question_value: QuestionValueUpdateGQLModel) -> QuestionValueResultGQLModel:
        loader = getLoaders(info).questionvalues
        row = await loader.update(question_value)
        result = QuestionValueResultGQLModel()
        result.msg = "ok"
        result.id = question_value.id
        if row is None:
            result.msg = "fail"           
        return result


