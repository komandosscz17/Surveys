# Surveys

#Časový harmonogram
Časový harmonogram:
9. 10. 2023 vytvoření githubu a harmonogramu.
16. 10. 2023 Obeznámení a porozumění projektu.
27. 11. 2023 Vytvoření RU operací.
15. 1. 2024  Alfa verze
21. 1. 2024 uzavření projektu
22. 1. 2024 počátek zkouškového období,

Zadání:
Entity (SurveyGQLModel, SurveyTypeGQLModel, AnswerGQLModel)
Entity (QuestionGQLModel, QuestionTypeGQLModel, QuestionValueGQLModel)
Modely v databázi pomocí SQLAlchemy, API endpoint typu GraphQL s pomocí knihovny Strawberry.
Přístup k databázi řešte důsledně přes AioDataloder, resp. (https://github.com/hrbolek/uoishelpers/blob/main/uoishelpers/dataloaders.py).
Zabezpečte kompletní CRUD operace nad entitami ExternalIdModel, ExternalIdTypeModel, ExternalIdCategoryModel
CUD operace jako návratový typ nejméně se třemi prvky id, msg a „entityresult“ (pojmenujte adekvátně podle dotčené entity), vhodné přidat možnost nadřízené entity, speciálně pro operaci D.
Řešte autorizaci operací (permission classes).
Kompletní CRUD dotazy na GQL v souboru externalids_queries.json (dictionary), jméno klíče nechť vhodně identifikuje operaci, hodnota je dictionary s klíči query (obsahuje parametrický dotaz) nebo mutation (obsahuje parametrické mutation) a variables (obsahuje dictionary jako testovací hodnoty).
Kompletní popisy API v kódu (description u GQLModelů) a popisy DB vrstvy (comment u DBModelů).
Zabezpečte více jak 90% code test coverage (standard pytest).
