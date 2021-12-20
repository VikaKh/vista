from drf_yasg import openapi

from core.serializers import AuthResponseSerializer, RegisterRequestSerializer


def error_schema(title):
    return openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(title=title, type=openapi.TYPE_STRING))


login_schema = {
    "operation_id": "Login",
    "tags": ["auth"],
    "responses": {
        200: AuthResponseSerializer,
        400: openapi.Schema(
            title="LoginError",
            type=openapi.TYPE_OBJECT,
            properties={
                "non_field_errors": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_STRING, enum=["Unable to log in with provided credentials."]
                    ),
                )
            },
        ),
    },
}

register_schema = {
    "operation_id": "Register",
    "tags": ["auth"],
    "request_body": RegisterRequestSerializer,
    "responses": {
        201: AuthResponseSerializer,
        400: openapi.Schema(
            title="RegistrationErrors",
            type=openapi.TYPE_OBJECT,
            properties={
                "username": error_schema("RegistrationUsernameError"),
                "password": error_schema("RegistrationPasswordError"),
                "first_name": error_schema("RegistrationFirstNameError"),
                "patronymic": error_schema("RegistrationPatronymicError"),
                "last_name": error_schema("RegistrationLastNameError"),
                "non_field_errors": error_schema("RegistrationNonFieldError"),
            },
        ),
    },
}
