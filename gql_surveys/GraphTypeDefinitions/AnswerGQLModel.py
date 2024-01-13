from typing import List, Union
import typing
import strawberry as strawberryA
from .extra import getLoaders, AsyncSessionFromInfo
import uuid
from .BaseGQLModel import BaseGQLModel
import datetime
from contextlib import asynccontextmanager

from .GraphResolvers import (
  
    resolve_id,
    resolve_lastchange,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_createdby,
    
  
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
class AnswerGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoaders(info).answers
           
    
  
    id = resolve_id
    lastchange = resolve_lastchange
    name_en = resolve_name_en
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    
    
    
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
        from .UserGQLModel import UserGQLModel
        return await UserGQLModel.resolve_reference(self.user_id)

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
    

@strawberryA.field(description="""Answer by user""")
async def answers_by_user(
        self, info: strawberryA.types.Info, user_id: uuid.UUID
    ) -> Union[AnswerGQLModel, None]:
        loader = getLoaders(info).answers
        result = await loader.filter_by(user_id=user_id)
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
    
@strawberryA.type
class AnswerResultGQLModel:
    id: uuid.UUID
    msg: str = None

    @strawberryA.field(description="""Result of answer operation""")
    async def answer(self, info: strawberryA.types.Info) -> Union[AnswerGQLModel, None]:
        result = await AnswerGQLModel.resolve_reference(info, self.id)
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
