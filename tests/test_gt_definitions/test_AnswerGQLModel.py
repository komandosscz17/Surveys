import pytest

from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    create_frontend_query,
    create_update_query
)
test_reference_answers = createResolveReferenceTest(
    table_name='surveyanswers', gqltype='AnswerGQLModel', 
    attributeNames=["id", "value", "aswered",'expired' "user_id",'question_id'  "created {id}", "lastchange", "createdby {id}", "changedby {id}"])
test_query_answer_by_id = createByIdTest(table_name="surveyanswers", queryEndpoint="answerById")
#test_query_answer_by_users = createPageTest(table_name="surveyanswers", queryEndpoint="answerByUser")


test_answer_update = create_update_query(query="""
    mutation($id: UUID!,$lastchange: DateTime! ) { 
        result: answerUpdate(answer: {id: $id, value: $value, lastchange: $lastchange}) { 
            id
            msg
            answer {
                id
                value
                
                              
            }
        }
    }
    """, 
    variables={"id": "e054d1a5-f259-429d-9f7a-f35d55caf2ab", "value": "10"},
    table_name="surveyanswers"
)

