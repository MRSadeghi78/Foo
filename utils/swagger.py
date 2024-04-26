import ast

from fastapi.openapi.utils import get_openapi


def generate_custom_openapi():
    """
        Generates a custom OpenAPI schema for the FastAPI application.

        Retrieves the existing schema if available, otherwise generates a new one based on the application routes.

        :return: Custom OpenAPI schema for the FastAPI application.
    """
    from main import app
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Foo",
        version="0.0.1",
        description="REST openapi specification",
        routes=app.routes,
        servers=[{"url": "http://127.0.0.1:8000"}]
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    openapi_schema["components"]["securitySchemes"] = {
        "tokenAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Token YOUR_TOKEN_HERE"
        }
    }
    openapi_schema["security"] = [{"tokenAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def generate_form_input(model_cls):
    """
        Generates form input for a given Pydantic model class.

        :param model_cls: Pydantic model class.
        :return: Form input schema for the given model class.
    """
    properties = {}
    json_schema = ast.literal_eval(model_cls.schema_json())
    for item in json_schema["properties"]:
        properties[item] = json_schema["properties"][item]
    return {
        "requestBody": {
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "properties": properties,
                        "required": json_schema["required"]
                    }
                }
            },
            "required": True
        }
    }
