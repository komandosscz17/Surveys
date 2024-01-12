import pytest

from .gt_utils import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    create_frontend_query,
    create_update_query
)

test_reference_surveytyepes =  createResolveReferenceTest(table_name='surveytypes', gqltype='SurveyTypeGQLModel', attributeNames=["id", "name", "lastchange"])

test_query_survey_type_by_id = createByIdTest(table_name="surveytypes", queryEndpoint="surveyTypeById")
test_query_survey_type_page = createPageTest(table_name="surveytypes", queryEndpoint="surveyTypePage")

#test_insert_survey_type = create_frontend_query(
#    query="""mutation ($id: UUID!, $name: String!) {
#        result: surveyTypeInsert(survey: {id: $id, name: $name,}) {
#            id
#            msg
#            survey {
#                id
#                name
#                
#            }
#        }
#    }""",
#    variables={"id": "f6f79926-ac0e-4833-9a38-4272cae33fa6", "name": "new name", "category_id": "5c8c4c5a-df3b-44a9-ab90-396bdc84542b"}
#) cekat na tobiho nez udela cru

#test_update_survey_type = create_update_query(
#    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
#        result: surveyTypeUpdate(project: {id: $id, name: $name, lastchange: $lastchange}) {
#            id
#            msg
#            project {
#                id
#                name
#            }
#        }
#    }""",
#    variables={"id": "2e1140f4-afb0-11ed-9bd8-0242ac110002", "name": "new name"},
#    table_name="surveytypes"
#)