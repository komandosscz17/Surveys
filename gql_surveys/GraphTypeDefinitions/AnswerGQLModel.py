from typing import List, Union
import typing
import strawberry as strawberryA
from gql_surveys.Dataloaders import getLoaders
import uuid
from .BaseGQLModel import BaseGQLModel
import datetime
from contextlib import asynccontextmanager

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
    
  
)  
from typing import Annotated

# @asynccontextmanager
# async def withInfo(info):
#     asyncSessionMaker = info.context["asyncSessionMaker"]
#     async with asyncSessionMaker() as session:
#         try:
#             yield session
#         finally:
#             pass
UserGQLModel = Annotated["UserGQLModel", strawberryA.lazy(".UserGQLModel")]
QuestionGQLModel = Annotated["QuestionGQLModel", strawberryA.lazy(".QuestionGQLModel")]
@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)
class AnswerGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoaders(info).answers
           
    
  
    id = resolve_id
    lastchange = resolve_lastchange
    changed_by = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    created_by = resolve_createdby
    user_id = resolve_user_id
    
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
    )  # v našem kontejneru
    async def question(self, info: strawberryA.types.Info) -> QuestionGQLModel:
        from .QuestionGQLModel import QuestionGQLModel
        return await QuestionGQLModel.resolve_reference(info, self.question_id)
    
#############################################################
#
# Queries
#
#############################################################
@strawberryA.field(description="""Answer by id""")
async def answer_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[AnswerGQLModel, None]:
        print(id, flush=True)
        return await AnswerGQLModel.resolve_reference(info=info ,id=id)
    
# @strawberryA.field(description="""Page of answers""")
# async def answer_page(
#         self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
#     ) -> typing.List[AnswerGQLModel]:
#         loader = getLoaders(info).answers
#         result = await loader.page(skip, limit)
#         return result

from dataclasses import dataclass
from .utils import createInputs

@createInputs
@dataclass
class AnswerWhereFilter:
    id: uuid.UUID
    value: str
    aswered: bool  #chyba není u mě, ale v pgadminu je psáno aswered
    expired: bool
    user_id: uuid.UUID
    question_id: uuid.UUID
    createdby: uuid.UUID
    changedby: uuid.UUID
    
@strawberryA.field(description="Retrieves the form type")
async def answer_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: typing.Optional[AnswerWhereFilter] = None
) -> typing.List[AnswerGQLModel]:
    wf = None if where is None else strawberryA.asdict(where)
    loader = getLoaders(info).answers
    result = await loader.page(skip, limit, where=wf)
    return result    
  



#############################################################
#
# Mutations
#
#############################################################
from typing import Optional
import datetime

@strawberryA.input
class AnswerUpdateGQLModel:
    lastchange: datetime.datetime
    id: typing.Optional[uuid.UUID] = strawberryA.field(description="primary key (UUID), could be client generated", default=None)
    value:typing.Optional[str] = None
    aswered: typing.Optional[bool] = None   
    expired: typing.Optional[bool] = None   
    

@strawberryA.input
class AnswerInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberryA.field(description="primary key (UUID), could be client generated", default=None)
    value:typing.Optional[str] = None
    aswered: typing.Optional[bool] = None   
    expired: typing.Optional[bool] = None   
    question_id: typing.Optional[uuid.UUID] = strawberryA.field(description="primary key (UUID), could be client generated", default=None)
    user_id:typing.Optional[uuid.UUID] = strawberryA.field(description="primary key (UUID), could be client generated", default=None)
  
    
@strawberryA.type
class AnswerResultGQLModel:
    id: uuid.UUID
    msg: str = None

    @strawberryA.field(description="""Result of answer operation""")
    async def answer(self, info: strawberryA.types.Info) -> Union[AnswerGQLModel, None]:
        result = await AnswerGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.input(description="Input structure - D operation")
class AnswerDeleteGQLModel:
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")

@strawberryA.type
class AnswerDeleteResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    msg: str = None 
    

@strawberryA.mutation(description="Deletes the answer")
async def answer_delete(
        self, info: strawberryA.types.Info, answer: AnswerDeleteGQLModel
) -> AnswerDeleteResultGQLModel:
    answerId = answer.id
    loader = getLoaders(info).answers
    row = await loader.delete(answerId)
    if not row:
        return AnswerDeleteResultGQLModel(id= answerId, msg="fail")
    result = AnswerDeleteResultGQLModel(id=answerId, msg="ok")
    return result      
    
@strawberryA.mutation(description="""Allows update a question.""")
async def answer_update(self, info: strawberryA.types.Info, answer: AnswerUpdateGQLModel) -> AnswerResultGQLModel:
        loader = getLoaders(info).answers
        row = await loader.update(answer)
        result = AnswerResultGQLModel(id=answer.id)
        result.msg = "ok"
        result.id = answer.id
        if row is None:
            result.msg = "fail"           
        return result

    
@strawberryA.mutation(description="""Allows update a question.""")
async def answer_insert(self, info: strawberryA.types.Info, answer: AnswerInsertGQLModel) -> AnswerResultGQLModel:
        loader = getLoaders(info).answers
        row = await loader.insert(answer)
        result = AnswerResultGQLModel(id=row.id, msg="ok")
        return result
