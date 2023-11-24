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

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass
        


QuestionGQLModel = Annotated["QuestionGQLModel", strawberryA.lazy(".QuestionGQLModel")]
@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a group""",
)
class SurveyGQLModel(BaseGQLModel):
    

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Survey name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""List""")
    async def questions(
        self, info: strawberryA.types.Info
    ) -> typing.List["QuestionGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveQuestionForSurvey(session, self.id)
            return result


#     @strawberryA.field(description="""List""")
#     async def editor(self, info: strawberryA.types.Info) -> 'SurveyEditorGQLModel':
#         return self

# @strawberryA.federation.type(keys=["id"], description="""Editor""") ###############
# class SurveyEditorGQLModel:
#     pass

#############################################################
#
# Queries
#
#############################################################
@strawberryA.field(description="""Finds a survey by its id""")
async def survey_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[SurveyGQLModel, None]:
        return await SurveyGQLModel.resolve_reference(info=info, id=id)

@strawberryA.field(description="""Page of surveys""")
async def survey_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> List[SurveyGQLModel]:
        loader = getLoaders(info).surveys
        result = await loader.page(skip, limit)
        return result

from gql_surveys.DBFeeder import randomSurveyData


@strawberryA.field(description="""Answer by id""")
async def load_survey(
        self, info: strawberryA.types.Info
    ) -> Union[SurveyGQLModel, None]:
        async with withInfo(info) as session:
            surveyID = await randomSurveyData(AsyncSessionFromInfo(info))
            result = await resolveSurveyById(session, surveyID)
            return result
        
        
###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################
from typing import Optional
import datetime

@strawberryA.input
class SurveyInsertGQLModel:
    name: str
    name_en: Optional[str] = ""

    type_id: Optional[strawberryA.ID] = None
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class SurveyUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    name: Optional[str] = None
    name_en: Optional[str] = None
    type_id: Optional[strawberryA.ID] = None
    
@strawberryA.type
class SurveyResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of survey operation""")
    async def survey(self, info: strawberryA.types.Info) -> Union[SurveyGQLModel, None]:
        result = await SurveyGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.mutation(description="""Creates new survey""")
async def survey_insert(self, info: strawberryA.types.Info, survey: SurveyInsertGQLModel) -> SurveyResultGQLModel:
        loader = getLoaders(info).surveys
        row = await loader.insert(survey)
        result = SurveyResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberryA.mutation(description="""Updates the survey""")
async def survey_update(self, info: strawberryA.types.Info, survey: SurveyUpdateGQLModel) -> SurveyResultGQLModel:
        loader = getLoaders(info).surveys
        row = await loader.update(survey)
        result = SurveyResultGQLModel()
        result.msg = "ok"
        result.id = survey.id
        if row is None:
            result.msg = "fail"           
        return result

@strawberryA.mutation(description="""Assigns the survey to the user. For all questions in the survey are created empty answers for the user.""")
async def survey_assing_to(self, info: strawberryA.types.Info, survey_id: strawberryA.ID, user_id: strawberryA.ID) -> SurveyResultGQLModel:
        loader = getLoaders(info).questions
        questions = await loader.filter_by(survey_id=survey_id)
        loader = getLoaders(info).answers
        for q in questions:
            exists = await loader.filter_by(question_id=q.id, user_id=user_id)
            if next(exists, None) is None:
                #user has not this particular question
                rowa = await loader.insert(None, {"question_id": q.id, "user_id": user_id})
        result = SurveyResultGQLModel()
        result.msg = "ok"
        result.id = survey_id
            
        return result