import pytest

from .gt_utils import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    create_frontend_query,
    create_update_query
)

test_reference_surveytyepes =  createResolveReferenceTest(table_name='surveytypes', gqltype='SurveyTypeGQLModel', attributeNames=["id", "name"])

test_query_survey_type_by_id = createByIdTest(table_name="surveytypes", queryEndpoint="surveyTypeById")
test_query_survey_type_page = createPageTest(table_name="surveytypes", queryEndpoint="surveyTypePage")

test_insert_survey_type = create_frontend_query(
   query="""mutation ($id: UUID!, $name: String!) {
       result: surveyTypeInsert(surveytype: {id: $id, name: $name,}) {
           id
           msg
           surveyType {
            id
            }
               
           
       }
   }""",
   variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new name"}
) 

test_surveytype_update = create_update_query(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            surveyTypeUpdate(surveytype: {id: $id, name: $name, lastchange: $lastchange}) {
          
            msg
            id
                surveyType {
             id
                }
            } 
        }
    """,
    variables={"id": "712029b6-2dbc-4952-9d3e-e897899edf0a", "name": "new name"},
    table_name="surveytypes"
)
