import strawberry as strawberryA
import uuid
import datetime

class BaseGQLModel:
    @classmethod
    def getLoader(cls, info):
        pass

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = cls.getLoader(info)
        result = await loader.load(id)
        if result is not None:
             result.__strawberry_definition__ = cls.__strawberry_definition_
        return result