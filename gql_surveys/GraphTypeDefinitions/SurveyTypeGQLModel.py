from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
import datetime
from contextlib import asynccontextmanager
from .BaseGQLModel import BaseGQLModel
from .extra import getLoaders, AsyncSessionFromInfo
from typing import List, Union
import typing
import strawberry as strawberryA
from .BaseGQLModel import BaseGQLModel
from contextlib import asynccontextmanager
import datetime
from typing import Annotated

from .GraphResolvers import (
    resolve_id,
    resolve_lastchange,
    resolve_name,
    resolve_name_en
    
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
    lastchange = resolve_lastchange
    name_en = resolve_name_en
#############################################################
#
# Queries
#
#############################################################

@strawberryA.field(description="""Page of survey types""")
async def survey_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> List[SurveyTypeGQLModel]:
        loader = getLoaders(info).surveytypes
        result = await loader.page(skip, limit)
        return result
    
@strawberryA.field(description="""Finds a survey type by its id""")
async def survey_type_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[SurveyTypeGQLModel, None]:
        return await SurveyTypeGQLModel.resolve_reference(info=info, id=id)
    
