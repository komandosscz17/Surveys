# Surveys

## Časový harmonogram
9.10.2023 vytvoření githubu a harmonogramu.<br>
16. 10. 2023 Obeznámení a porozumění projektu.<br>
27. 11. 2023 Vytvoření RU operací.<br>
15. 1. 2024  Alfa verze<br>
21. 1. 2024 uzavření projektu<br>
22. 1. 2024 počátek zkouškového období,<br>

## Zadání:
Entity (SurveyGQLModel, SurveyTypeGQLModel, AnswerGQLModel)<br>
Entity (QuestionGQLModel, QuestionTypeGQLModel, QuestionValueGQLModel)<br>
Modely v databázi pomocí SQLAlchemy, API endpoint typu GraphQL s pomocí knihovny Strawberry.<br>
Přístup k databázi řešte důsledně přes AioDataloder, resp. (https://github.com/hrbolek/uoishelpers/blob/main/uoishelpers/dataloaders.py).<br>
Zabezpečte kompletní CRUD operace nad entitami ExternalIdModel, ExternalIdTypeModel, ExternalIdCategoryModel<br>
CUD operace jako návratový typ nejméně se třemi prvky id, msg a „entityresult“ (pojmenujte adekvátně podle dotčené entity), vhodné přidat možnost nadřízené entity, speciálně pro operaci D.
Řešte autorizaci operací (permission classes).<br>
Kompletní CRUD dotazy na GQL v souboru externalids_queries.json (dictionary), jméno klíče nechť vhodně identifikuje operaci, hodnota je dictionary s klíči query (obsahuje parametrický dotaz) nebo mutation (obsahuje parametrické mutation) a variables (obsahuje dictionary jako testovací hodnoty).<br>
Kompletní popisy API v kódu (description u GQLModelů) a popisy DB vrstvy (comment u DBModelů).<br>
Zabezpečte více jak 90% code test coverage (standard pytest).<br>
