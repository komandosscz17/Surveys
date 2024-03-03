from typing import List, Union
import strawberry as strawberryA
import datetime
import uuid
from contextlib import asynccontextmanager
from .GraphResolvers import (
    resolve_id,
    resolve_user_id,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    
)   


from gql_surveys.Dataloaders import getLoaders




from .UserGQLModel import UserGQLModel
from .QuestionValueGQLModel import QuestionValueGQLModel
from .QuestionGQLModel import QuestionGQLModel
from .QuestionTypeGQLModel import QuestionTypeGQLModel
from .AnswerGQLModel import AnswerGQLModel
from .SurveyGQLModel    import SurveyGQLModel
from .SurveyTypeGQLModel import SurveyTypeGQLModel 
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
    )
    survey_by_id = survey_by_id
    survey_page = survey_page
    
    from .QuestionGQLModel import (
        question_by_id,
        question_page
    )
    question_by_id = question_by_id
    question_page = question_page
    
    from .QuestionTypeGQLModel import (
        question_type_by_id,
        question_type_page
    )
    
    question_type_by_id = question_type_by_id
    question_by_id = question_by_id

    from .QuestionValueGQLModel import (
        questioValue_by_id,
        questionValue_page
    )
    questioValue_by_id = questioValue_by_id
    questionValue_page = questionValue_page
    
    from .AnswerGQLModel import(
        answer_by_id,
        answer_page
        
    )
    answer_by_id = answer_by_id
    answer_page = answer_page
    




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
    survey_assing_to ,
    survey_delete
    )
    survey_insert = survey_insert
    survey_update = survey_update
    survey_assing_to = survey_assing_to
    survey_delete = survey_delete

    from .SurveyTypeGQLModel import (
    surveyType_insert,
    surveyType_update,
    surveytype_delete,
    )
    surveyType_insert = surveyType_insert
    surveyType_update = surveyType_update
    surveytype_delete = surveytype_delete

    from .AnswerGQLModel import (
    answer_update,
    answer_insert,
    answer_delete
    )
    answer_update = answer_update
    answer_insert = answer_insert
    answer_delete = answer_delete

    from .QuestionTypeGQLModel import (
    questionType_insert,
    questionType_update,
    
    )
    questionType_insert = questionType_insert
    questionType_update = questionType_update
    
    from .QuestionGQLModel import (
    question_insert,
    question_update,
    question_delete,
    )
    question_insert = question_insert
    question_update = question_update
    question_delete = question_delete
    

    from .QuestionValueGQLModel import (
     question_value_insert,
     question_value_update,
     question_value_delete
    ) 
    question_value_insert = question_value_insert
    question_value_update = question_value_update
    question_value_delete = question_value_delete



    

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,), mutation=Mutation)
