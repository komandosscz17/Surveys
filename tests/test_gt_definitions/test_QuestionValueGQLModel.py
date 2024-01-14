import pytest

from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    create_frontend_query,
    create_update_query,
    create_delete_query
)
test_reference_questionvalues = createResolveReferenceTest(
    table_name='surveyquestionvalues', gqltype='QuestionValueGQLModel', 
    attributeNames=["id", "name",])
# test_query_questionvalue_by_id = createByIdTest(table_name="surveyquestionvalues", queryEndpoint="questionValueById")
# test_query_questionvalue_page = createPageTest(table_name="surveyquestionvalues", queryEndpoint="questionValuePage")


test_questionValue_insert = create_frontend_query(query="""
    mutation($id: UUID!, $question_id: UUID!, $name: String! ) { 
        result: questionValueInsert(questionValue: {id: $id, name: $name, questionId: $question_id}) { 
            id
            msg
            question {
                id
                name
                lastchange
                              
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new survey", "question_id": "5b7e4ae7-9bb9-4e2f-829b-c2763ac1092e"},
    asserts=[]
)



test_questionvalue_update = create_update_query(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            questionValueUpdate(questionValue: {id: $id, name: $name, lastchange: $lastchange}) {
                id
                msg
                question {
                    id
                    name
                }
            }
        }
    """,
    variables={"id": "5dee5260-7cd9-4433-b735-679871153205", "name": "new name"},
    table_name="surveyquestionvalues"
)
# dodelat delete
# test_questionvalue_delete = create_delete_query(
#     query="""
#         mutation($id: UUID!) {
#             questionValueDelete(questionvalue: {id: $id}) {
#                 id
#                 msg
#                 question {
#                     id
#                     name
#                 }
#             }
#         }
#     """,
#     variables={"id": "5dee5260-7cd9-4433-b735-679871153205"},
#     table_name="surveyquestionvalues"
# )



