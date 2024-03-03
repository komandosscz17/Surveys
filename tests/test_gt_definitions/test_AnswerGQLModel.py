import pytest

from .gt_utils import (
    createByIdTestAnswer, 
    createByIdTest,  
    createResolveReferenceTestAnswer, 
    create_frontend_query,
    create_update_query,
    create_delete_query

)

test_reference_answers = createResolveReferenceTestAnswer(
    table_name='surveyanswers', gqltype='AnswerGQLModel', 
    attributeNames=["id", "value"])
test_query_answer_by_id = createByIdTestAnswer(table_name="surveyanswers", queryEndpoint="answerById")



test_answer_update = create_update_query(query="""
    mutation($id: UUID!,$lastchange: DateTime!, $value: String ) { 
        result: answerUpdate(answer: {id: $id, value: $value, lastchange: $lastchange}) { 
            id
            msg
            answer {
                id
               
                
                
                              
            }
        }
    }
    """, 
    variables={"id": "e054d1a5-f259-429d-9f7a-f35d55caf2ab", "value": "10"},
    table_name="surveyanswers"
)

test_answer_delete = create_delete_query(
    query="""
        mutation($id: UUID!) {
            answerDelete(answer: {id: $id}) {
                id
                msg
                
            }
        }
    """,
    variables={"id": "ad0f53fb-240b-47de-ab1d-871bbde6f972"},
    table_name="surveyanswers"
)

