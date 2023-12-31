from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
from typing import Annotated
import datetime
from contextlib import asynccontextmanager
from .BaseGQLModel import BaseGQLModel
from .extra import getLoaders

from .GraphResolvers import (
    resolveAnswersForQuestion,
     resolve_id,
    resolve_lastchange,
    resolve_name,
    resolve_name_en
    
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
    @classmethod
    def getLoader(cls, info):
        return getLoaders(info).questions
    id = resolve_id
    name = resolve_name
    lastchange = resolve_lastchange
    name_en = resolve_name_en
    
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
        from .SurveyGQLModel import SurveyGQLModel
        result = await SurveyGQLModel.resolve_reference(info, self.survey_id)
        return result

    @strawberryA.field(description="""Type of question""")
    async def type(
        self, info: strawberryA.types.Info
    ) -> typing.Union["QuestionTypeGQLModel", None]:
        from .QuestionTypeGQLModel import QuestionTypeGQLModel
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
@strawberryA.field(description="""Question by id""")
async def question_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[QuestionGQLModel, None]:
        return await QuestionGQLModel.resolve_reference(info = info, id=id)


#############################################################
#
# Mutations
#
#############################################################
from typing import Optional
import datetime

@strawberryA.input
class QuestionInsertGQLModel:
    name: typing.Optional[str] = None
    survey_id: typing.Optional[uuid.UUID] = None
    name_en: typing.Optional[str] = ""
    type_id: typing.Optional[uuid.UUID] = None
    order: typing.Optional[int] = strawberryA.field(description="Position in parent entity", default=None)
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")

@strawberryA.input
class QuestionUpdateGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    name: typing.Optional[str] = None
    name_en: typing.Optional[str] = None
    type_id: typing.Optional[uuid.UUID] = None
    order: typing.Optional[int] = None

@strawberryA.type
class QuestionResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberryA.field(description="""Result of question operation""")
    async def question(self, info: strawberryA.types.Info) -> Union[QuestionGQLModel, None]:
        result = await QuestionGQLModel.resolve_reference(info, self.id)
        return result
    

@strawberryA.mutation(description="""Updates question value / possible answer""")
async def question_value_delete(self, info: strawberryA.types.Info, question_value_id: uuid.UUID) -> QuestionResultGQLModel:
        loader = getLoaders(info).questionvalues
        row = await loader.load(question_value_id)
        await loader.delete(question_value_id)
        result = QuestionResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        if row is None:
            result.msg = "fail"           
        return result

@strawberryA.mutation(description="""Creates new question in the survey""")
async def question_insert(self, info: strawberryA.types.Info, question: QuestionInsertGQLModel) -> QuestionResultGQLModel:
        loader = getLoaders(info).questions
        row = await loader.insert(question)
        result = QuestionResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberryA.mutation(description="""Updates question""")
async def question_update(self, info: strawberryA.types.Info, question: QuestionUpdateGQLModel) -> QuestionResultGQLModel:
        loader = getLoaders(info).questions
        row = await loader.update(question)
        result = QuestionResultGQLModel()
        result.msg = "ok"
        result.id = question.id
        if row is None:
            result.msg = "fail"           
        return result
    