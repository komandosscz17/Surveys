from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
from functools import cache
from aiodataloader import DataLoader
import datetime
import aiohttp
import asyncio
import os
import logging
from uoishelpers.resolvers import select, update, delete


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

from functools import cache