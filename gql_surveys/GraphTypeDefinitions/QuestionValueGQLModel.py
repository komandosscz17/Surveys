from typing import List, Union
import typing
import strawberry as strawberryA
from .BaseGQLModel import BaseGQLModel
from contextlib import asynccontextmanager
import datetime
from typing import Annotated
from gql_surveys.Dataloaders import getLoaders
import uuid

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
    resolve_order

)

        
QuestionGQLModel = Annotated["QuestionGQLModel", strawberryA.lazy(".QuestionGQLModel")]
@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)
class QuestionValueGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoaders(info).questionvalues
    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    name_en = resolve_name_en
    order = resolve_order
    

   
#############################################################
#
# Queries
#
#############################################################
@strawberryA.field(description="""Finds a questionvalue by its id""")
async def questioValue_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> typing.Optional[QuestionValueGQLModel]:
        result = await QuestionValueGQLModel.resolve_reference(info=info,  id=id)
        return result
    
@strawberryA.field(description="""Question which has this possible answer""")
async def question(self, info: strawberryA.types.Info) -> Union[QuestionGQLModel, None]:
        from .QuestionGQLModel import QuestionGQLModel
        result = await QuestionGQLModel.resolve_reference(info, self.question_id)
        return result


from dataclasses import dataclass
from .utils import createInputs

QuestionWhereFilter = Annotated["QuestionWhereFilter", strawberryA.lazy(".QuestionGQLModel")]

@createInputs
@dataclass
class QuestionValueWhereFilter:
    name: str
    name_en: str
    id: uuid.UUID
    created_by: uuid.UUID
    changed_by: uuid.UUID

    # Using QuestionWhereFilter directly without the Annotated wrapper
    # surveys: QuestionWhereFilter

@strawberryA.field(description="Allows showing and filtering guestion_value information")
async def questionValue_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: typing.Optional[QuestionValueWhereFilter] = None
) -> typing.List[QuestionValueGQLModel]:
    loader = getLoaders(info).questionvalues
    wf = None if where is None else strawberryA.asdict(where)
    result = await loader.page(skip=skip, limit=limit, where=wf)
    return result
#############################################################
#
# Models
#
#############################################################
from typing import Optional
import datetime


@strawberryA.input
class QuestionValueInsertGQLModel:
    question_id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    name: typing.Optional[str] = strawberryA.field(description="name of the associated question value", default=None)
    name_en: typing.Optional[str] = strawberryA.field(description="The english name of the associated question value", default=None) 
    order: typing.Optional[int] = strawberryA.field(description="Position in parent entity", default=None)
    id: typing.Optional[uuid.UUID] = strawberryA.field(description="primary key (UUID), could be client generated", default=None)

@strawberryA.input
class QuestionValueUpdateGQLModel:
    lastchange: datetime.datetime = strawberryA.field(description="Timestamp of the last change")
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    name: typing.Optional[str] = strawberryA.field(description="name of the associated question value update", default=None)
    name_en: typing.Optional[str] = strawberryA.field(description="The english name of the associated question value update", default=None) 
    order: typing.Optional[int] = strawberryA.field(description="Position in parent entity", default=None)
    
@strawberryA.input(description="Input structure - D operation")
class QuestionValueDeleteGQLModel:
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    
@strawberryA.type
class QuestionValueResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    msg: str = strawberryA.field(description="check message", default=None) 

    @strawberryA.field(description="""Result of question operation""")
    async def question(self, info: strawberryA.types.Info) -> Union[QuestionValueGQLModel, None]:
        result = await QuestionValueGQLModel.resolve_reference(info, self.id)
        return result
@strawberryA.type
class QuestionValueDeleteResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    msg: str = strawberryA.field(description="check message", default=None)


#############################################################
#
# Mutations
#
#############################################################



@strawberryA.mutation(description="""Creates new question value for closed question""")
async def question_value_insert(self, info: strawberryA.types.Info, question_value: QuestionValueInsertGQLModel) -> QuestionValueResultGQLModel:
        loader = getLoaders(info).questionvalues
        row = await loader.insert(question_value)
        result = QuestionValueResultGQLModel(id=row.id, msg="ok")
        return result

@strawberryA.mutation(description="""Updates question value / possible answer""")
async def question_value_update(self, info: strawberryA.types.Info, question_value: QuestionValueUpdateGQLModel) -> QuestionValueResultGQLModel:
    loader = getLoaders(info).questionvalues
    row = await loader.update(question_value)
    result = QuestionValueResultGQLModel(id=question_value.id, msg="ok")  # <-- Provide 'id' during instance creation
    if row is None:
        result.msg = "fail"           
    return result

@strawberryA.mutation(description="Delete the authorization user")
async def question_value_delete(
        self, info: strawberryA.types.Info, questionvalue: QuestionValueDeleteGQLModel
) -> QuestionValueDeleteResultGQLModel:
    questionvalueId = questionvalue.id
    loader = getLoaders(info).questionvalues
    row = await loader.delete(questionvalueId)
    if not row:
        return QuestionValueDeleteResultGQLModel(id= questionvalueId, msg="fail, user not found")
    result = QuestionValueDeleteResultGQLModel(id=questionvalueId, msg="ok")
    return result


