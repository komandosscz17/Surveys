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


test_questiontype_insert = create_frontend_query(query="""
    mutation($id: UUID!, $name: String! ) { 
        result: questionTypeInsert(questionType   : {id: $id, name: $name}) { 
            id
            msg
            
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new survey"},
    asserts=[]
)



test_questiontyoe_update = create_update_query(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            questionTypeUpdate(questionType : {id: $id, name: $name, lastchange: $lastchange}) {
                id
                msg
                
            }
        }
    """,
    variables={"id": "ad0f53fb-240b-47de-ab1d-871bbde6f973", "name": "new name"},
    table_name="surveyquestiontypes"
)



