from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
from functools import cache
from aiodataloader import DataLoader
from uoishelpers.resolvers import select, update, delete
import logging


from gql_surveys.DBDefinitions import (
    SurveyModel, 
    SurveyTypeModel, 
    QuestionModel,
    QuestionTypeModel,
    QuestionValueModel, 
    AnswerModel
    )

dbmodels = {
    "surveys": SurveyModel, 
    "surveytypes": SurveyTypeModel, 
    "questions": QuestionModel, 
    "questiontypes": QuestionTypeModel, 
    "questionvalues": QuestionValueModel, 
    "answers": AnswerModel
    
}
class Loaders:
    authorizations = None
    requests = None
    histories = None
    forms = None
    formtypes = None
    formcategories = None
    sections = None
    parts = None
    items = None
    itemtypes = None
    itemcategories = None
    pass

from uoishelpers.dataloaders import createIdLoader


async def createLoaders(asyncSessionMaker, models=dbmodels):
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        print("creating loader ", key)
        attrs[key] = property(cache(createLambda(key, DBModel)))
    
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }
def getLoaders(info):
    return info.context['all']

def AsyncSessionFromInfo(info):
    print(
        "obsolete function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]

demouser = {
    "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
    "name": "John",
    "surname": "Newbie",
    "email": "john.newbie@world.com",
    "roles": [
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                "name": "administrátor"
            }
        },
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
                "name": "rektor"
            }
        }
    ]
}

def getUserFromInfo(info):
    context = info.context
    #print(list(context.keys()))
    user = context.get("user", None)
    if user is None:
        request = context.get("request", None)
        assert request is not None, "request is missing in context :("
        user = request.scope.get("user", None)
        assert user is not None, "missing user in context or in request.scope"
    logging.debug("getUserFromInfo", user)
    return user

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }