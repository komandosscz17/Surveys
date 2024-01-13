import sys
import asyncio
import pytest
import logging
import uuid
import sqlalchemy
import json
import re

# setting path
#sys.path.append("../gql_events")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_surveys.GraphTypeDefinitions import schema

from ..shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    create_context,
    create_schema_function
)
from tests.client import create_client_function
        

def createByIdTest(table_name, queryEndpoint, attributeNames=["id", "name"]):

    @pytest.mark.asyncio
    async def result_test():
        def test_result(response):
            print("response", response)
            errors = response.get("errors", None)
            assert errors is None

            response_data = response.get("data", None)
            assert response_data is not None

            response_data = response_data[queryEndpoint]
            assert response_data is not None

            for attribute in attributeNames:
                assert response_data[attribute] == f'{data_row[attribute]}'

        schema_executor = create_schema_function()
        client_executor = create_client_function()

        data = get_demodata()
        data_row = data[table_name][0]
        content = "{" + ", ".join(attributeNames) + "}"
        query = "query($id: UUID!){" f"{queryEndpoint}(id: $id)" f"{content}" "}"

        variable_values = {"id": f'{data_row["id"]}'}

        
        logging.debug(f"query {query} with {variable_values}")

        response = await schema_executor(query, variable_values)
        test_result(response)
        response = await client_executor(query, variable_values)
        test_result(response)

    return result_test

def createByIdTestAnswer(table_name, queryEndpoint, attributeNames=["id", "value"]):

    @pytest.mark.asyncio
    async def result_test():
        def test_result(response):
            print("response", response)
            errors = response.get("errors", None)
            assert errors is None

            response_data = response.get("data", None)
            assert response_data is not None

            response_data = response_data[queryEndpoint]
            assert response_data is not None

            for attribute in attributeNames:
                assert response_data[attribute] == f'{data_row[attribute]}'

        schema_executor = create_schema_function()
        client_executor = create_client_function()

        data = get_demodata()
        data_row = data[table_name][0]
        content = "{" + ", ".join(attributeNames) + "}"
        query = "query($id: UUID!){" f"{queryEndpoint}(id: $id)" f"{content}" "}"

        variable_values = {"id": f'{data_row["id"]}'}

        
        logging.debug(f"query {query} with {variable_values}")

        response = await schema_executor(query, variable_values)
        test_result(response)
        response = await client_executor(query, variable_values)
        test_result(response)

    return result_test


def createPageTest(table_name, queryEndpoint, attributeNames=["id"]):
    @pytest.mark.asyncio
    async def result_test() -> None:
        def test_result(response) -> None:
            print("response", response)
            errors = response.get("errors", None)
            assert errors is None

            response_data = response.get("data", None)
            assert response_data is not None

            response_data = response_data.get(queryEndpoint, None)
            assert response_data is not None
            data_rows = data[table_name]

            for row_a, row_b in zip(response_data, data_rows):
                for attribute in attributeNames:
                    assert row_a[attribute] == f'{row_b[attribute]}'

        schema_executor = create_schema_function()
        client_executor = create_client_function()

        data = get_demodata()

        content = "{" + ", ".join(attributeNames) + "}"
        query = "query{ " f"{queryEndpoint} {content}" "}"

       

        response = await schema_executor(query)
        test_result(response)
        response = await client_executor(query)
        test_result(response)

    return result_test
# 

def createResolveReferenceTest(table_name, gqltype, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():

        def testResult(resp):
            print(resp)
            errors = resp.get("errors", None)
            assert errors is None
            respdata = resp.get("data", None)
            assert respdata is not None

            logging.info(respdata)
            respdata = respdata.get('_entities', None)
            assert respdata is not None

            assert len(respdata) == 1
            respdata = respdata[0]

            assert respdata['id'] == rowid

        schemaExecutor = create_schema_function()
        clientExecutor = create_client_function()

        content = "{" + ", ".join(attributeNames) + "}"

        data = get_demodata()
        table = data[table_name]
        for row in table:
            rowid = f"{row['id']}"

            # query = (
            #     'query($id: UUID!) { _entities(representations: [{ __typename: '+ f'"{gqltype}", id: $id' + 
            #     ' }])' +
            #     '{' +
            #     f'...on {gqltype}' + content +
            #     '}' + 
            #     '}')

            # variable_values = {"id": rowid}

            query = ("query($rep: [_Any!]!)" + 
                "{" +
                "_entities(representations: $rep)" +
                "{"+
                f"    ...on {gqltype} {content}"+
                "}"+
                "}"
            )
            
            variable_values = {"rep": [{"__typename": f"{gqltype}", "id": f"{rowid}"}]}

            logging.info(f"query representations {query} with {variable_values}")
            resp = await clientExecutor(query, {**variable_values})
            testResult(resp)
            resp = await schemaExecutor(query, {**variable_values})
            testResult(resp)

        print(f"{gqltype}_representation")
        

    return result_test
def createResolveReferenceTestAnswer(table_name, gqltype, attributeNames=["id", "value"]):
    @pytest.mark.asyncio
    async def result_test():

        def testResult(resp):
            print(resp)
            errors = resp.get("errors", None)
            assert errors is None
            respdata = resp.get("data", None)
            assert respdata is not None

            logging.info(respdata)
            respdata = respdata.get('_entities', None)
            assert respdata is not None

            assert len(respdata) == 1
            respdata = respdata[0]

            assert respdata['id'] == rowid

        schemaExecutor = create_schema_function()
        clientExecutor = create_client_function()

        content = "{" + ", ".join(attributeNames) + "}"

        data = get_demodata()
        table = data[table_name]
        for row in table:
            rowid = f"{row['id']}"

            # query = (
            #     'query($id: UUID!) { _entities(representations: [{ __typename: '+ f'"{gqltype}", id: $id' + 
            #     ' }])' +
            #     '{' +
            #     f'...on {gqltype}' + content +
            #     '}' + 
            #     '}')

            # variable_values = {"id": rowid}

            query = ("query($rep: [_Any!]!)" + 
                "{" +
                "_entities(representations: $rep)" +
                "{"+
                f"    ...on {gqltype} {content}"+
                "}"+
                "}"
            )
            
            variable_values = {"rep": [{"__typename": f"{gqltype}", "id": f"{rowid}"}]}

            logging.info(f"query representations {query} with {variable_values}")
            resp = await clientExecutor(query, {**variable_values})
            testResult(resp)
            resp = await schemaExecutor(query, {**variable_values})
            testResult(resp)

        print(f"{gqltype}_representation")
        

    return result_test




def create_frontend_query(query="{}", variables={}, asserts=[]):
    @pytest.mark.asyncio
    async def test_frontend_query() -> None:
        logging.debug("create_frontend_query")
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)
        context_value = create_context(async_session_maker)
        logging.debug(f"query {query} with {variables}")
        print(f"query {query} with {variables}")

        #append(query_name=f"query", query=query, variables=variables)
        response = await schema.execute(
            query=query,
            variable_values=variables,
            context_value=context_value
        )

        assert response.errors is None, response.errors[0]
        response_data = response.data
        logging.debug(f"response_data: {response_data}")
        for a in asserts:
            a(response_data)

    return test_frontend_query


def create_update_query(query="{}", variables={}, table_name=""):

    @pytest.mark.asyncio
    async def test_update() -> None:
        logging.debug("test_update")
        assert variables.get("id", None) is not None, "variables must contain id"
        variables["id"] = uuid.UUID(f"{variables['id']}")
        assert "$lastchange: DateTime!" in query, "query must contain $lastchange: DateTime!"
        assert "lastchange: $lastchange" in query, "query must use lastchange: $lastchange"
        assert table_name != "", "missing table name"

        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        print("variables['id']", variables, flush=True)
        statement = sqlalchemy.text(f"SELECT id, lastchange FROM {table_name} WHERE id=:id").bindparams(id=variables["id"])
        print("statement", statement, flush=True)
        async with async_session_maker() as session:
            rows = await session.execute(statement)
            row = rows.first()

            print("row", row)
            id = row[0]
            lastchange = row[1]

            print(f"id {id} lastchange {lastchange}")

        variables["lastchange"] = lastchange
        variables["id"] = f'{variables["id"]}'
        context_value = create_context(async_session_maker)
        logging.debug(f"query {query} with {variables}")
        print(f"query {query} with {variables}")

        #append(query_name=f"query_{table_name}", mutation=query, variables=variables)


        response = await schema.execute(
            query=query,
            variable_values=variables,
            context_value=context_value
        )

        assert response.errors is None
        response_data = response.data
        assert response_data is not None
        print(f"response_data: {response_data}")
        keys = list(response_data.keys())
        assert len(keys) == 1, "expected update test has one result"
        key = keys[0]
        result = response_data.get(key, None)
        assert result is not None, f"{key} is None (test update) with {query}"
        entity = None
        for key, value in result.items():
            print(f"key {key} value {value}, {type(value)}")
            if isinstance(value, dict):
                entity = value
                break
        assert entity is not None, f"expected entity in response to {query}"

        for key, value in entity.items():
            if key in ["id", "lastchange"]:
                continue
            print("attribute check", type(key), f"[{key}] is {value} ?= {variables[key]}")
            assert value == variables[key], f"test update failed {value} != {variables[key]}"

    return test_update