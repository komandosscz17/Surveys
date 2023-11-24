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
class QuestionTypeGQLModel(BaseGQLModel):


    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Survey name""")
    def name(self) -> str:
        return self.name
#############################################################
#
# Queries
#
#############################################################
@strawberryA.field(description="""Question type by id""")
async def question_type_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[QuestionTypeGQLModel, None]:
        return await QuestionTypeGQLModel.resolve_reference(info, id)

@strawberryA.field(description="""Question type by id""")
async def question_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> List[QuestionTypeGQLModel]:
        loader = getLoaders(info).questiontypes
        result = await loader.page(skip, limit)
        return result