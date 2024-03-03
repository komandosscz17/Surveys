from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
from typing import Annotated
import datetime
from contextlib import asynccontextmanager
from .BaseGQLModel import BaseGQLModel
from gql_surveys.Dataloaders import getLoaders

from .GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_user_id,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    resolve_order,
    
    
)


# @asynccontextmanager
# async def withInfo(info):
#     asyncSessionMaker = info.context["asyncSessionMaker"]
#     async with asyncSessionMaker() as session:
#         try:
#             yield session
#         finally:
#             pass

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
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    name_en = resolve_name_en
    order = resolve_order


    @strawberryA.field(description="""List of answers related to the user""")
    async def answers(
        self, info: strawberryA.types.Info
    ) -> List["AnswerGQLModel"]:
        loader = getLoaders(info).answers
        result = await loader.filter_by(question_id = self.id)
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
        loader = getLoaders(info).questionvalues
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

from dataclasses import dataclass
from .utils import createInputs

@createInputs
@dataclass
class QuestionWhereFilter:
    name: str
    name_en: str
    id: uuid.UUID
    survey_id: uuid.UUID
    type_id: uuid.UUID
    createdby: uuid.UUID
    order: int


@strawberryA.field(description="Allows showing and filtering question information")
async def question_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: typing.Optional[QuestionWhereFilter] = None
) -> typing.List[QuestionGQLModel]:
    wf = None if where is None else strawberryA.asdict(where)
    loader = getLoaders(info).questions
    result = await loader.page(skip, limit, where=wf)
    return result    





from typing import Optional
import datetime

#############################################################
#
# Models
#
#############################################################

@strawberryA.input
class QuestionInsertGQLModel:
    name: typing.Optional[str] = strawberryA.field(description="Name of question", default=None)
    survey_id: typing.Optional[uuid.UUID] = strawberryA.field(description="The ID of the associated survey", default=None)
    name_en: typing.Optional[str] = strawberryA.field(description="The english name of the associated question", default=None)
    type_id: typing.Optional[uuid.UUID] = strawberryA.field(description="The ID of the question type", default=None)
    order: typing.Optional[int] = strawberryA.field(description="Position in parent entity", default=None)
    id: typing.Optional[uuid.UUID] = strawberryA.field(description="primary key (UUID), could be client generated", default=None)   
@strawberryA.input
class QuestionUpdateGQLModel:
    lastchange: datetime.datetime = strawberryA.field(description="Timestamp of the last change")
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    name: typing.Optional[str] = strawberryA.field(description="Name of question", default=None)
    name_en: typing.Optional[str] = strawberryA.field(description="The english name of the associated question", default=None)
    type_id: typing.Optional[uuid.UUID] =  strawberryA.field(description="The ID of the question type", default=None)
    order: typing.Optional[int] = strawberryA.field(description="Position in parent entity", default=None)
    

@strawberryA.type
class QuestionResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None) 

    @strawberryA.field(description="""Result of question operation""")
    async def question(self, info: strawberryA.types.Info) -> Union[QuestionGQLModel, None]:
        result = await QuestionGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.input(description="Input structure - D operation")
class QuestionDeleteGQLModel:
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")

@strawberryA.type
class QuestionDeleteResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)
    
#############################################################
#
# Mutations
#
#############################################################
@strawberryA.mutation(description="Delete the question")
async def question_delete(
        self, info: strawberryA.types.Info, question: QuestionDeleteGQLModel
) -> QuestionDeleteResultGQLModel:
    questionId = question.id
    loader = getLoaders(info).questions
    row = await loader.delete(questionId)
    if not row:
        return QuestionDeleteResultGQLModel(id= questionId, msg="fail, user not found")
    result = QuestionDeleteResultGQLModel(id=questionId, msg="ok")
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
    