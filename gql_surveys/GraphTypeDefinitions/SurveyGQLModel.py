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

# @asynccontextmanager
# async def withInfo(info):
#     asyncSessionMaker = info.context["asyncSessionMaker"]
#     async with asyncSessionMaker() as session:
#         try:
#             yield session
#         finally:
#             pass
        


QuestionGQLModel = Annotated["QuestionGQLModel", strawberryA.lazy(".QuestionGQLModel")]
@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a group""",
)
class SurveyGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        
        return getLoaders(info).surveys
        
    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    name_en = resolve_name_en
   
    
    @strawberryA.field(description="""List""")
    async def questions(
        self, info: strawberryA.types.Info
    ) -> typing.List["QuestionGQLModel"]:
        loader = getLoaders(info).questions
        rows = await loader.filter_by(survey_id = self.id)
        result = list(rows)
        print (result)
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
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> typing.Optional[SurveyGQLModel]:
        result = await SurveyGQLModel.resolve_reference(info=info,  id=id)
        return result

@strawberryA.field(description="""Page of surveys""")
async def survey_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> typing.List[SurveyGQLModel]:
        loader = getLoaders(info).surveys
        result = await loader.page(skip, limit)
        return result

from gql_surveys.DBFeeder import randomSurveyData


        
        
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
    name: typing.Optional[str] = None
    name_en: typing.Optional[str] = ""
    type_id: typing.Optional[uuid.UUID] = None
    id: typing.Optional[uuid.UUID] = strawberryA.field(description="primary key (UUID), could be client generated", default=None)
@strawberryA.input
class SurveyUpdateGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    name: typing.Optional[str] = None
    name_en: typing.Optional[str] = None
    type_id: typing.Optional[uuid.UUID] = None
    
@strawberryA.type
class SurveyResultGQLModel:
    id: strawberryA.ID = strawberryA.field(default=None, description="primary key value")
    msg: str = None

    @strawberryA.field(description="""Result of survey operation""")
    async def survey(self, info: strawberryA.types.Info) -> typing.Optional[SurveyGQLModel]:
        result = await SurveyGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.mutation(description="""Creates new survey""")
async def survey_insert(self, info: strawberryA.types.Info, survey: SurveyInsertGQLModel) -> SurveyResultGQLModel:
        loader = getLoaders(info).surveys
        row = await loader.insert(survey)
        result = SurveyResultGQLModel(id=row.id, msg="ok")
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