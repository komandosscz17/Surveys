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
    resolve_user_id,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    
    
)
        
@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a group""",
)
class SurveyTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoaders(info).surveytypes

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

# @strawberryA.field(description="""Page of survey types""")
# async def survey_type_page(
#         self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
#     ) -> List[SurveyTypeGQLModel]:
#         loader = getLoaders(info).surveytypes
#         result = await loader.page(skip, limit)
#         return result
    
@strawberryA.field(description="""Finds a survey type by its id""")
async def survey_type_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[SurveyTypeGQLModel, None]:
        return await SurveyTypeGQLModel.resolve_reference(info=info, id=id)

from dataclasses import dataclass
from .utils import createInputs

SurveyWhereFilter = Annotated["SurveyWhereFilter", strawberryA.lazy(".SurveyGQLModel")]

@createInputs
@dataclass
class SurveyTypeWhereFilter:
    name: str
    name_en: str
    id: uuid.UUID
    createdby: uuid.UUID
    changedby: uuid.UUID

    # Using QuestionWhereFilter directly without the Annotated wrapper
    # forms: SurveyWhereFilter

@strawberryA.field(description="Allows showing and filtering survey_type information")
async def survey_type_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: typing.Optional[SurveyTypeWhereFilter] = None
) -> typing.List[SurveyTypeGQLModel]:
    loader = getLoaders(info).surveytypes
    wf = None if where is None else strawberryA.asdict(where)
    result = await loader.page(skip=skip, limit=limit, where=wf)
    return result
#############################################################
#
# Models
#
#############################################################
@strawberryA.input
class SurveyTypeUpdateGQLModel:
    lastchange: datetime.datetime = strawberryA.field(description="Timestamp of the last change")
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    name: typing.Optional[str] = strawberryA.field(description="Name of SurveyTypeUpdate")
    name_en: typing.Optional[str] = strawberryA.field(description="english name of SurveyTypeUpdate")

@strawberryA.input
class SurveyTypeInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberryA.field(description="primary key (UUID), could be client generated", default=None)
    name:typing.Optional[str] = strawberryA.field(description="Name of SurveyTypeInsert")
    
@strawberryA.type
class SurveyTypeResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)
    
    @strawberryA.field(description="subject of operation")
    async def survey_type(self, info: strawberryA.types.Info) -> SurveyTypeGQLModel:
        return await SurveyTypeGQLModel.resolve_reference(info, self.id)

@strawberryA.input(description="Input structure - D operation")
class SurveytypeDeleteGQLModel:
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")

@strawberryA.type
class SurveytypeDeleteResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)
    
#############################################################
#
# Mutations
#
#############################################################


@strawberryA.mutation(description="Delete the surveytype")
async def surveytype_delete(
        self, info: strawberryA.types.Info, surveytype: SurveytypeDeleteGQLModel
) -> SurveytypeDeleteResultGQLModel:
    surveytypeId = surveytype.id
    loader = getLoaders(info).surveytypes
    row = await loader.delete(surveytypeId)
    if not row:
        return SurveytypeDeleteResultGQLModel(id= surveytypeId, msg="fail")
    result = SurveytypeDeleteResultGQLModel(id=surveytypeId, msg="ok")
    return result
    
@strawberryA.mutation(description="""Allows update a question.""")
async def surveyType_update(self, info: strawberryA.types.Info, surveytype: SurveyTypeUpdateGQLModel) -> SurveyTypeResultGQLModel:
        loader = getLoaders(info).surveytypes
        row = await loader.update(surveytype)
        result = SurveyTypeResultGQLModel(id=surveytype.id)
        result.msg = "ok"
        result.id = surveytype.id
        if row is None:
            result.msg = "fail"           
        return result

@strawberryA.mutation(description="""Allows update a question.""")
async def surveyType_insert(self, info: strawberryA.types.Info, surveytype: SurveyTypeInsertGQLModel) -> SurveyTypeResultGQLModel:
        loader = getLoaders(info).surveytypes
        row = await loader.insert(surveytype)
        result = SurveyTypeResultGQLModel(id=row.id, msg="ok")
        return result