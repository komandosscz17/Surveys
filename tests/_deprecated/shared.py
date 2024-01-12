import sqlalchemy
import sys
import asyncio
import logging
# setting path
#sys.path.append("../gql_surveys")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_surveys.DBDefinitions import BaseModel
from gql_surveys.DBDefinitions import AnswerModel, SurveyModel, SurveyTypeModel, QuestionModel, QuestionTypeModel, QuestionValueModel

async def prepare_in_memory_sqllite():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker

    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker

from gql_surveys.DBFeeder import get_demodata

async def prepare_demodata(async_session_maker):
    data = get_demodata()

    from uoishelpers.feeders import ImportModels

    await ImportModels(
        async_session_maker,
        [
            AnswerModel, 
            SurveyModel, 
            SurveyTypeModel, 
            QuestionModel, 
            QuestionTypeModel, 
            QuestionValueModel
        ],
        data,
    )


from gql_surveys.Dataloaders import createLoadersContext

def create_context(async_session_maker, with_user=True):

    loaders_context = createLoadersContext(async_session_maker)
    user = {
        "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
        "name": "John",
        "surname": "Newbie",
        "email": "john.newbie@world.com"
    }
    if with_user:
        loaders_context["user"] = user

    return loaders_context

def create_info(async_session_maker, with_user=True):
    class Request():
        @property
        def headers(self):
            return {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}

    class Info():
        @property
        def context(self):
            context = create_context(async_session_maker, with_user=with_user)
            context["request"] = Request()
            return context

    return Info()


from gql_surveys.GraphTypeDefinitions import schema


def create_schema_function():
    async def result(query: str, variables: dict = None) -> dict:
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)
        context_value = create_context(async_session_maker)
        logging.debug(f"query {query} with {variables}")
        print(f"query {query} with {variables}")
        response = await schema.execute(
            query=query,
            variable_values=variables,
            context_value=context_value
        )

        assert response.errors is None
        response_data = response.data
        logging.debug(f"response data: {response_data}")
        result = {"data": response_data, "errors": response.errors}
        return {"data": response_data, "errors": response.errors}

    return result