from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
import datetime
from contextlib import asynccontextmanager
from .BaseGQLModel import BaseGQLModel
from gql_surveys.Dataloaders import getLoaders
from typing import List, Union
import typing
import strawberry as strawberryA
from .BaseGQLModel import BaseGQLModel
from contextlib import asynccontextmanager
import datetime
from typing import Annotated

from .GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_authorization_id,
    resolve_user_id,
    resolve_accesslevel,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    createRootResolver_by_page,
)

@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a group""",
)
class QuestionTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoaders(info).questiontypes
    
    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    name_en = resolve_name_en
#############################################################
#
# Queries
#
#############################################################
@strawberryA.field(description="""Question type by id""")
async def question_type_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[QuestionTypeGQLModel, None]:
        return await QuestionTypeGQLModel.resolve_reference(info=info, id=id)

@strawberryA.field(description="""Question type by id""")
async def question_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> List[QuestionTypeGQLModel]:
        loader = getLoaders(info).questiontypes
        result = await loader.page(skip, limit)
        return result

#############################################################
#
# Mutations
#
#############################################################
@strawberryA.input
class QuestionTypeUpdateGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    name: typing.Optional[str] = None
    name_en: typing.Optional[str] = None
    
    
@strawberryA.input
class QuestionTypeInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberryA.field(description="primary key (UUID), could be client generated", default=None)
    name:typing.Optional[str] = None

@strawberryA.type
class QuestionTypeResultGQLModel:
    id: uuid.UUID
    msg: str = None

    
@strawberryA.mutation(description="""Allows update a question.""")
async def questionType_update(self, info: strawberryA.types.Info, questionType: QuestionTypeUpdateGQLModel) -> QuestionTypeResultGQLModel:
        loader = getLoaders(info).questiontypes
        row = await loader.update(questionType)
        result = QuestionTypeResultGQLModel(id=questionType.id)
        result.msg = "ok"
        result.id = questionType.id
        if row is None:
            result.msg = "fail"           
        return result

@strawberryA.mutation(description="""Allows update a question.""")
async def questionType_insert(self, info: strawberryA.types.Info, questionType: QuestionTypeInsertGQLModel) -> QuestionTypeResultGQLModel:
        loader = getLoaders(info).questiontypes
        row = await loader.insert(questionType)
        result = QuestionTypeResultGQLModel(id=row.id, msg="ok")
        return result