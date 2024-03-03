
import strawberry
import uuid
import datetime
import typing

from uoishelpers.resolvers import (
        create1NGetter,
        createEntityByIdGetter,
        createEntityGetter,
        createInsertResolver,
        createUpdateResolver,
    )

from gql_surveys.DBDefinitions import (
        
        
        AnswerModel,
        
    )
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]


@strawberry.field(description="""Entity primary key""")
def resolve_id(self) -> uuid.UUID:
    return self.id

@strawberry.field(description="""Time of last update""")
def resolve_lastchange(self) -> datetime.datetime:
    return self.lastchange

@strawberry.field(description="""Name """)
def resolve_name(self) -> str:
    return self.name

@strawberry.field(description="""English name""")
def resolve_name_en(self) -> str:
    result = self.name_en if self.name_en else ""
    return result
@strawberry.field(description="""order of questiuons""")
def resolve_order(self) -> int:
    return self.order 
# @strawberry.field(description="""Authorization id """)
# def resolve_authorization_id(self) -> uuid.UUID:
#     return self.authorization_id





async def resolve_user(user_id):
    from .UserGQLModel import UserGQLModel
    result = None if user_id is None else await UserGQLModel.resolve_reference(user_id)
    return result


@strawberry.field(description="""User ID """)
async def resolve_user_id(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.user_id)



# @strawberry.field(description="""Level of authorization""")
# def resolve_accesslevel(self) -> int:
#     return self.accesslevel


@strawberry.field(description="""Time of entity introduction""")
def resolve_created(self) -> typing.Optional[datetime.datetime]:
    return self.created


@strawberry.field(description="""Who created entity""")
async def resolve_createdby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.createdby)


@strawberry.field(description="""Who made last change""")
async def resolve_changedby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.changedby)


# answers
resolveAnswersForUser = create1NGetter(AnswerModel, foreignKeyName="user_id")

resolve_result_id: uuid.UUID = strawberry.field(description="primary key of CU operation object")
resolve_result_msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")

# fields for mutations insert and update
resolve_insert_id = strawberry.field(graphql_type=typing.Optional[uuid.UUID], description="primary key (UUID), could be client generated", default=None)
resolve_update_id = strawberry.field(graphql_type=uuid.UUID, description="primary key (UUID), identifies object of operation")
resolve_update_lastchage = strawberry.field(graphql_type=datetime.datetime, description="timestamp of last change = TOKEN")

# fields for mutation result
resolve_cu_result_id = strawberry.field(graphql_type=uuid.UUID, description="primary key of CU operation object")
resolve_cu_result_msg = strawberry.field(graphql_type=str, description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")


def createRootResolver_by_id(scalarType: None, description="Retrieves item by its id"):
    assert scalarType is not None

    @strawberry.field(description=description)
    async def by_id(
            self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[scalarType]:
        result = await scalarType.resolve_reference(info=info, id=id)
        return result

    return by_id





