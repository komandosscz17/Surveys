import pytest

from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    create_frontend_query,
    create_update_query
)
test_reference_questions = createResolveReferenceTest(
    table_name='surveyquestions', gqltype='QuestionGQLModel', 
    attributeNames=["id", "name",])
test_query_questiomn_by_id = createByIdTest(table_name="surveyquestions", queryEndpoint="questionById")



test_question_insert = create_frontend_query(query="""
    mutation($id: UUID!,$type_id: UUID!,  $name: String!, $survey_id: UUID! ) { 
        result: questionInsert(question: {id: $id, name: $name, typeId: $type_id, surveyId: $survey_id}) { 
            id
            msg
            question {
                id
                lastchange
                              
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new_questions", "type_id": "712029b6-2dbc-4952-9d3e-e897899edf0a", "survey_id": "910d54a9-7f2e-41ca-b811-3c600ef82fda"},
    asserts=[]
)



test_question_update = create_update_query(
    query="""
        mutation($id: UUID!, $lastchange: DateTime!, $name: String!) {
            questionUpdate(question: {id: $id, name: $name, lastchange: $lastchange}) {
                id
                msg
                question {
                    id
                    name
                }
            }
        }
    """,
    variables={"id": "5b7e4ae7-9bb9-4e2f-829b-c2763ac1092e", "name": "new name"},
    table_name="surveyquestions "
)



