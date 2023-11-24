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
    resolveSurveyById,
    resolveQuestionById,
    resolveAnswerById,
    resolveQuestionTypeById,
    resolveAnswersForQuestion,
    resolveAnswersForUser,
    resolveQuestionForSurvey,
)
        
@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a group""",
)
class SurveyTypeGQLModel(BaseGQLModel):
    

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Survey name""")
    def name(self) -> str:
        return self.name
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
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[SurveyTypeGQLModel, None]:
        return await SurveyTypeGQLModel.resolve_reference(info, id)
    
