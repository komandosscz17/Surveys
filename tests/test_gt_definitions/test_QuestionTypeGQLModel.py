import pytest

from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    create_frontend_query,
    create_update_query
)
test_reference_questiontypes = createResolveReferenceTest(
    table_name='surveyquestiontypes', gqltype='QuestionTypeGQLModel', 
    attributeNames=["id", "name",])
test_query_questiontype_by_id = createByIdTest(table_name="surveyquestiontypes", queryEndpoint="questionTypeById")
test_query_questiontype_page = createPageTest(table_name="surveyquestiontypes", queryEndpoint="questionTypePage")


# test_questiontype_insert = create_frontend_query(query="""
#     mutation($id: UUID!,$type_id: UUID!, $name: String! ) { 
#         result: surveyInsert(survey: {id: $id, name: $name, typeId: $type_id}) { 
#             id
#             msg
#             survey {
#                 id
#                 name
#                 lastchange
                              
#             }
#         }
#     }
#     """, 
#     variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new survey", "type_id": "712029b6-2dbc-4952-9d3e-e897899edf0a"},
#     asserts=[]
# )



# test_survey_update = create_update_query(
#     query="""
#         mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
#             surveyUpdate(survey: {id: $id, name: $name, lastchange: $lastchange}) {
#                 id
#                 msg
#                 survey {
#                     id
#                     name
#                 }
#             }
#         }
#     """,
#     variables={"id": "910d54a9-7f2e-41ca-b811-3c600ef82fda", "name": "new name"},
#     table_name="surveys"
# )



