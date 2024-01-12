import sqlalchemy
import sys
import asyncio

# setting path

#sys.path.append("../gql_surveys")

import pytest


# from ..uoishelpers.uuid import UUIDColumn

from gql_surveys.DBDefinitions import BaseModel
from gql_surveys.DBDefinitions import AnswerModel, SurveyModel, SurveyTypeModel, QuestionModel, QuestionTypeModel, QuestionValueModel

from tests._deprecated.shared import prepare_demodata, prepare_in_memory_sqllite, get_demodata


@pytest.mark.asyncio
async def test_table_users_feed():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()


from gql_surveys.DBDefinitions import ComposeConnectionString


def test_connection_string():
    connectionString = ComposeConnectionString()

    assert "://" in connectionString
    assert "@" in connectionString



from gql_surveys.DBDefinitions import startEngine


@pytest.mark.asyncio
async def test_table_start_engine():
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None

from gql_surveys.DBFeeder import initDB


@pytest.mark.asyncio
async def test_initDB():
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None
    await initDB(async_session_maker)
