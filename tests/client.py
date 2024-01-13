import logging
import json
from tests.introspection import query

def create_gql_client():

    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import gql_surveys.DBDefinitions

    def ComposeCString():
        return "sqlite+aiosqlite:///:memory:"

    gql_surveys.DBDefinitions.ComposeConnectionString = ComposeCString

    import main

    client = TestClient(main.app, raise_server_exceptions=False)

    return client


def create_client_function():
    client = create_gql_client()

    async def result(query, variables={}):
        json = {
            "query": query,
            "variables": variables
        }
        headers = {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
        logging.debug(f"query client for {query} with {variables}")

        response = client.post("/gql", headers=headers, json=json)
        return response.json()

    return result



def update_introspection_query():
    from .introspection import query
    client = create_gql_client()
    inputjson = {"query": query, "variables": {}}
    response = client.post("/gql", headers={}, json=inputjson)
    responsejson = response.json()
    data = responsejson["data"]
    print(responsejson)
    with open("./introspectionquery.json", "w", encoding="utf-8") as f:
        datastr = json.dumps(data)
        f.write(datastr)


update_introspection_query()