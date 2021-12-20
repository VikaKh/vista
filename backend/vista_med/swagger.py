from django.conf import settings
from drf_yasg import openapi

from core.swagger import error_schema

from .serializers import (
    EmployeeSerializer,
    GetFinancingSourcesInfoRequestSerializer,
    GetFinancingSourcesInfoResponseSerializer,
    PatientAppointmentsInfoGetRequestParamSerializer,
    PatientAppointmentsInfoGetRequestResponseSerializer,
    PatientSerializer,
)

try:
    _max_date_delta = settings.PATIENT_APPOINTMENTS_INFO_REQUEST_DATE_PARAMS_MAX_DELTA_IN_DAYS
except AttributeError:
    from . import DEFAULT_PATIENT_APPOINTMENTS_INFO_REQUEST_DATE_PARAMS_MAX_DELTA_IN_DAYS

    _max_date_delta = DEFAULT_PATIENT_APPOINTMENTS_INFO_REQUEST_DATE_PARAMS_MAX_DELTA_IN_DAYS
if _max_date_delta is None:
    _delta_right_boundary_msg = ""
else:
    _delta_right_boundary_msg = f"and <= {_max_date_delta} (date range up to {_max_date_delta + 1} days)"

get_patient_appointments_info_schema = {
    "operation_id": "GetPatientAppointmentsInfo",
    "operation_description": f"""
        Get info about patient appointments for time period. Returns list of dicts.

        Date delta to_* - from_* must be => 0{_delta_right_boundary_msg}.
        At least one parameters from the list (from_datetime, to_datetime, from_date, to_date) must be given.
    """,
    "tags": ["api"],
    "query_serializer": PatientAppointmentsInfoGetRequestParamSerializer,
    "responses": {
        200: PatientAppointmentsInfoGetRequestResponseSerializer,
    },
}


get_employee_by_fullname_schema = {
    "tags": ["api"],
    "manual_parameters": [
        openapi.Parameter("full_name", openapi.IN_QUERY, "full name of employee", type=openapi.TYPE_STRING)
    ],
    "responses": {
        200: EmployeeSerializer,
    },
}


get_patient_by_fullname_schema = {
    "tags": ["api"],
    "manual_parameters": [
        openapi.Parameter("full_name", openapi.IN_QUERY, "full name of patient", type=openapi.TYPE_STRING)
    ],
    "responses": {
        200: PatientSerializer,
    },
}


get_financing_sources_info_schema = {
    "operation_id": "GetFinancingSourcesInfo",
    "tags": ["api"],
    "query_serializer": GetFinancingSourcesInfoRequestSerializer,
    "responses": {
        200: openapi.Schema(
            title="GetFinancingSourcesInfoResponse",
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                title="FinancingSource",
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, read_only=True),
                    "name": openapi.Schema(type=openapi.TYPE_STRING, read_only=True),
                    "total_count": openapi.Schema(type=openapi.TYPE_INTEGER, read_only=True),
                },
            ),
        ),
        400: openapi.Schema(
            title="GetFinancingSourcesInfoError",
            type=openapi.TYPE_OBJECT,
            properties={
                "from_datetime": error_schema("GetFinancingSourcesInfoFromDatetimeError"),
                "to_datetime": error_schema("GetFinancingSourcesInfoToDatetimeError"),
            },
        ),
    },
}
