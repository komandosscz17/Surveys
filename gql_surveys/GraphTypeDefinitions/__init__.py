from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
import datetime
from contextlib import asynccontextmanager
from .BaseGQLModel import BaseGQLModel
from .GraphResolvers import (
    resolveSurveyById,
    resolveQuestionById,
    resolveAnswerById,
    resolveQuestionTypeById,
    resolveAnswersForQuestion,
    resolveAnswersForUser,
    resolveQuestionForSurvey,
)   


from .extra import getLoaders, AsyncSessionFromInfo

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

from .extra import getLoaders, AsyncSessionFromInfo
from .UserGQLModel import UserGQLModel
from .SurveyGQLModel import SurveyGQLModel
from .SurveyTypeGQLModel import SurveyTypeGQLModel
from .QuestionTypeGQLModel import QuestionTypeGQLModel
from .QuestionValueGQLModel import QuestionValueGQLModel
from .QuestionGQLModel import QuestionGQLModel
from .AnswerGQLModel import AnswerGQLModel

from gql_surveys.DBFeeder import randomSurveyData
#############################################################
#
# Queries
#
#############################################################

@strawberryA.type(description="""Type for query root""")
class Query:
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
    
    @strawberryA.field(description="""Finds a survey by its id""")
    async def survey_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[SurveyGQLModel, None]:
        return await SurveyGQLModel.resolve_reference(info, id)

    @strawberryA.field(description="""Page of surveys""")
    async def survey_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> List[SurveyGQLModel]:
        loader = getLoaders(info).surveys
        result = await loader.page(skip, limit)
        return result
    
    @strawberryA.field(description="""Question by id""")
    async def question_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[QuestionGQLModel, None]:
        return await QuestionGQLModel.resolve_reference(info, id)

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

    @strawberryA.field(description="""Answer by id""")
    async def answer_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[AnswerGQLModel, None]:
        print(id, flush=True)
        return await AnswerGQLModel.resolve_reference(info, id)
    

    @strawberryA.field(description="""Answer by user""")
    async def answers_by_user(
        self, info: strawberryA.types.Info, user_id: strawberryA.ID
    ) -> Union[AnswerGQLModel, None]:
        loader = getLoaders(info).answers
        result = await loader.filter_by(user_id=user_id)
        return result  

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

@strawberryA.input
class AnswerUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    value: Optional[str] = None
    aswered: Optional[bool] = None   
    expired: Optional[bool] = None   
    
@strawberryA.type
class AnswerResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of answer operation""")
    async def answer(self, info: strawberryA.types.Info) -> Union[AnswerGQLModel, None]:
        result = await AnswerGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input
class QuestionInsertGQLModel:
    name: str
    survey_id: strawberryA.ID
    name_en: Optional[str] = ""
    type_id: Optional[strawberryA.ID] = None
    order: Optional[int] = 1
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class QuestionUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    name: Optional[str] = None
    name_en: Optional[str] = None
    type_id: Optional[strawberryA.ID] = None
    order: Optional[int] = None

@strawberryA.type
class QuestionResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of question operation""")
    async def question(self, info: strawberryA.types.Info) -> Union[QuestionGQLModel, None]:
        result = await QuestionGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.input
class QuestionValueInsertGQLModel:
    question_id: strawberryA.ID
    name: str
    name_en: Optional[str] = ""   
    order: Optional[int] = 1
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class QuestionValueUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    name: Optional[str] = None
    name_en: Optional[str] = None
    order: Optional[int] = None

@strawberryA.type
class QuestionValueResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of question operation""")
    async def question(self, info: strawberryA.types.Info) -> Union[QuestionValueGQLModel, None]:
        result = await QuestionValueGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.type
class Mutation:
    @strawberryA.mutation(description="""Creates new question value for closed question""")
    async def question_value_insert(self, info: strawberryA.types.Info, question_value: QuestionValueInsertGQLModel) -> QuestionValueResultGQLModel:
        loader = getLoaders(info).questionvalues
        row = await loader.insert(question_value)
        result = QuestionValueResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="""Updates question value / possible answer""")
    async def question_value_update(self, info: strawberryA.types.Info, question_value: QuestionValueUpdateGQLModel) -> QuestionValueResultGQLModel:
        loader = getLoaders(info).questionvalues
        row = await loader.update(question_value)
        result = QuestionValueResultGQLModel()
        result.msg = "ok"
        result.id = question_value.id
        if row is None:
            result.msg = "fail"           
        return result

    @strawberryA.mutation(description="""Updates question value / possible answer""")
    async def question_value_delete(self, info: strawberryA.types.Info, question_value_id: strawberryA.ID) -> QuestionResultGQLModel:
        loader = getLoaders(info).questionvalues
        row = await loader.load(question_value_id)
        await loader.delete(question_value_id)
        result = QuestionResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        if row is None:
            result.msg = "fail"           
        return result

    @strawberryA.mutation(description="""Creates new question in the survey""")
    async def question_insert(self, info: strawberryA.types.Info, question: QuestionInsertGQLModel) -> QuestionResultGQLModel:
        loader = getLoaders(info).questions
        row = await loader.insert(question)
        result = QuestionResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="""Updates question""")
    async def question_update(self, info: strawberryA.types.Info, question: QuestionUpdateGQLModel) -> QuestionResultGQLModel:
        loader = getLoaders(info).questions
        row = await loader.update(question)
        result = QuestionResultGQLModel()
        result.msg = "ok"
        result.id = question.id
        if row is None:
            result.msg = "fail"           
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

    @strawberryA.mutation(description="""Allows update a question.""")
    async def answer_update(self, info: strawberryA.types.Info, answer: AnswerUpdateGQLModel) -> AnswerResultGQLModel:
        loader = getLoaders(info).answers
        row = await loader.update(answer)
        result = AnswerResultGQLModel()
        result.msg = "ok"
        result.id = answer.id
        if row is None:
            result.msg = "fail"           
        return result


###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,), mutation=Mutation)
