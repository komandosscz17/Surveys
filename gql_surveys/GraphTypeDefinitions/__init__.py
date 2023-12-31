from typing import List, Union
import strawberry as strawberryA
import datetime
import uuid
from contextlib import asynccontextmanager
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


from .UserGQLModel import UserGQLModel
from .QuestionValueGQLModel import QuestionValueGQLModel
from .QuestionGQLModel import QuestionGQLModel
from .QuestionTypeGQLModel import QuestionTypeGQLModel
from .AnswerGQLModel import AnswerGQLModel
from .SurveyGQLModel    import SurveyGQLModel
from .SurveyTypeGQLModel import SurveyTypeGQLModel 
from gql_surveys.DBFeeder import randomSurveyData
#############################################################
#
# Queries
#
#############################################################

@strawberryA.type(description="""Type for query root""")
class Query:
    

    from .SurveyTypeGQLModel import(
    survey_type_page,
    survey_type_by_id,
    )

    survey_type_page = survey_type_page
    survey_type_by_id = survey_type_by_id
    
    from .SurveyGQLModel import (
        survey_by_id,
        survey_page,
        load_survey
    )

    survey_by_id = survey_by_id
    survey_page = survey_page
    load_survey = load_survey
    
    from .QuestionGQLModel import (
        question_by_id
    )
    question_by_id = question_by_id
    
    from .QuestionTypeGQLModel import (
        question_type_by_id,
        question_type_page
    )
    
    question_type_by_id = question_type_by_id
    question_by_id = question_by_id

    from .AnswerGQLModel import(
        answer_by_id,
        answers_by_user
    )
    answer_by_id = answer_by_id
    answers_by_user = answers_by_user




#############################################################
#
# Mutations
#
#############################################################

from typing import Optional
import datetime
@strawberryA.type(description="""Type for mutation root""")
class Mutation:

    from .SurveyGQLModel import (
    survey_insert,
    survey_update,
    survey_assing_to 
    )
    survey_insert = survey_insert
    survey_update = survey_update
    survey_assing_to = survey_assing_to

    from .AnswerGQLModel import (
    answer_update
    )
    answer_update = answer_update

    from .QuestionGQLModel import (
    question_insert,
    question_update,
    question_value_delete
    )
    question_insert = question_insert
    question_update = question_update
    question_value_delete = question_value_delete

    from .QuestionValueGQLModel import (
     question_value_insert,
     question_value_update,
    ) 
    question_value_insert = question_value_insert
    question_value_update = question_value_update




    

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,), mutation=Mutation)
