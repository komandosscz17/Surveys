#   from ast import Call
#     from typing import Coroutine, Callable, Awaitable, Union, List
#     import uuid
#     import datetime
#     from sqlalchemy.future import select
#     from sqlalchemy.orm import selectinload, joinedload
#     from sqlalchemy.ext.asyncio import AsyncSession
#     import strawberry
#     import typing
#     from uoishelpers.resolvers import (
#         create1NGetter,
#         createEntityByIdGetter,
#         createEntityGetter,
#         createInsertResolver,
#         createUpdateResolver,
#     )
#     from uoishelpers.resolvers import putSingleEntityToDb

#     UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]


#     from gql_surveys.DBDefinitions import BaseModel

#     from gql_surveys.DBDefinitions import (
#         SurveyModel,
#         QuestionModel,
#         AnswerModel,
#         QuestionTypeModel,
#     )

#     @strawberry.field(description="""Entity primary key""")
#     def resolve_id(self) -> uuid.UUID:
#         return self.id

#     @strawberry.field(description="""Name """)
#     def resolve_name(self) -> str:
#         return self.name

#     @strawberry.field(description="""English name""")
#     def resolve_name_en(self) -> str:
#         return self.name_en

#     @strawberry.field(description="""Time of last update""")
#     def resolve_lastchange(self) -> datetime.datetime:
#         return self.lastchange

#     @strawberry.field(description="""Who made last change""")
#     async def resolve_changedby(self) -> typing.Optional["UserGQLModel"]:
#         return await resolve_user(self.changedby)
#     async def resolve_user(user_id):
#         from .UserGQLModel import UserGQLModel
#         result = None if user_id is None else await UserGQLModel.resolve_reference(user_id)
#         return result
#     @strawberry.field(description="""Time of entity introduction""")
#     def resolve_created(self) -> typing.Optional[datetime.datetime]:
#         return self.created
#     @strawberry.field(description="""Who created entity""")
#     async def resolve_createdby(self) -> typing.Optional["UserGQLModel"]:
#         return await resolve_user(self.createdby)
#     # users
#     #resolveUserPaged = createEntityGetter(UserModel)
#     #resolveUserById = createEntityByIdGetter(UserModel)
#     #resolveUserSurvey = createInsertResolver(UserModel)

#     resolveAnswersForUser = create1NGetter(AnswerModel, foreignKeyName="user_id")

#     # surveys
#     resolveSurveyPaged = createEntityGetter(SurveyModel)
#     resolveSurveyById = createEntityByIdGetter(SurveyModel)
#     resolveInsertSurvey = createInsertResolver(SurveyModel)



#     resolveQuestionForSurvey = create1NGetter(QuestionModel, foreignKeyName="survey_id")

#     # questions
#     resolveQuestionPaged = createEntityGetter(QuestionModel)
#     resolveQuestionById = createEntityByIdGetter(QuestionModel)
#     resolveInsertQuestion = createInsertResolver(QuestionModel)

#     resolveAnswersForQuestion = create1NGetter(AnswerModel, foreignKeyName="question_id")


#     # question types
#     resolveQuestionTypePaged = createEntityGetter(QuestionTypeModel)
#     resolveQuestionTypeById = createEntityByIdGetter(QuestionTypeModel)
#     resolveInsertQuestionType = createInsertResolver(QuestionTypeModel)


#     # answers
#     resolveAnswerPaged = createEntityGetter(AnswerModel)
#     resolveAnswerById = createEntityByIdGetter(AnswerModel)
#     resolveAnswerQuestion = createInsertResolver(AnswerModel)