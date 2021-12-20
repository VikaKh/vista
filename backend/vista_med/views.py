from datetime import timedelta

from django.conf import settings
from django.db.models import F, Q, Value
from django.db.models.functions import Concat
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters as rest_filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from . import swagger
from .models import Employee, Patient, Organisation, OrganisationStructure
from .serializers import (
    OrganisationSerializer,
    OrganisationStructureSerializer,
    EmployeeSerializer,
    GetFinancingSourcesInfoRequestSerializer,
    GetFinancingSourcesInfoResponseSerializer,
    PatientAppointmentsInfoGetRequestParamSerializer,
    PatientAppointmentsInfoGetRequestResponseSerializer,
    PatientSerializer,
)
from .services import get_financing_sources_with_count, get_patient_appointments_for_period


class OrganisationsView(generics.ListAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    filter_backends = [rest_filters.SearchFilter]
    search_fields = ("full_name",)


class OrganisationStructuresView(generics.ListAPIView):
    queryset = OrganisationStructure.objects.all()
    serializer_class = OrganisationStructureSerializer
    filter_backends = (filters.DjangoFilterBackend, rest_filters.SearchFilter)
    filterset_fields = ("organisation",)
    search_fields = ("name",)


class EmployeeView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("organisation", "organisation_structure")

    def filter_queryset(self, queryset):
        q = super().filter_queryset(queryset).select_related("organisation", "organisation_structure")
        full_name = self.request.query_params.get("full_name")
        if not full_name:
            return q
        parts = full_name.split()
        return q.annotate(
            full_name=Concat(F("first_name"), Value(" "), F("last_name"), Value(" "), F("patr_name"))
        ).filter(*[Q(full_name__icontains=part) for part in parts])

    @swagger_auto_schema(**swagger.get_employee_by_fullname_schema)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GetPatientAppointmentsInfo(APIView):
    try:
        max_date_delta_in_days = settings.PATIENT_APPOINTMENTS_INFO_REQUEST_DATE_PARAMS_MAX_DELTA_IN_DAYS
    except AttributeError:
        from . import DEFAULT_PATIENT_APPOINTMENTS_INFO_REQUEST_DATE_PARAMS_MAX_DELTA_IN_DAYS

        max_date_delta_in_days = DEFAULT_PATIENT_APPOINTMENTS_INFO_REQUEST_DATE_PARAMS_MAX_DELTA_IN_DAYS

    _max_timedelta = None if max_date_delta_in_days is None else timedelta(days=max_date_delta_in_days)

    @swagger_auto_schema(**swagger.get_patient_appointments_info_schema)
    def get(self, request):
        serializer = PatientAppointmentsInfoGetRequestParamSerializer(
            data=request.query_params, max_date_delta_in_days=self.max_date_delta_in_days
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        from_dt = validated_data.get("from_datetime") or validated_data.get("from_date")
        to_dt = validated_data.get("to_datetime") or validated_data.get("to_date")

        if self.max_date_delta_in_days is not None:
            if from_dt is None and to_dt is None:
                raise RuntimeError("serializer is broken")
            if from_dt is None:
                from_dt = to_dt - self._max_timedelta
            elif to_dt is None:
                to_dt = from_dt + self._max_timedelta

        qs = get_patient_appointments_for_period(
            status=validated_data["status"],
            from_dt=from_dt,
            to_dt=to_dt,
            executing_employee=validated_data.get("employee"),
            patient=validated_data.get("patient"),
            organisation=validated_data.get("organisation"),
            organisation_structure=validated_data.get("organisation_structure"),
        )
        return Response(PatientAppointmentsInfoGetRequestResponseSerializer(qs, many=True).data)


class PatientView(APIView):
    @swagger_auto_schema(**swagger.get_patient_by_fullname_schema)
    def get(self, request):
        full_name = request.query_params.get("full_name")
        parts = full_name.split()
        patients = Patient.objects.annotate(
            full_name=Concat(F("first_name"), Value(" "), F("last_name"), Value(" "), F("patr_name"))
        ).filter(*[Q(full_name__icontains=part) for part in parts])
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)


class GetFinancingSourcesInfoView(APIView):
    try:
        max_date_delta_in_days = settings.FINANCING_SOURCES_INFO_REQUEST_DATE_PARAMS_MAX_DELTA_IN_DAYS
    except AttributeError:
        from . import DEFAULT_FINANCING_SOURCES_INFO_REQUEST_DATE_PARAMS_MAX_DELTA_IN_DAYS

        max_date_delta_in_days = DEFAULT_FINANCING_SOURCES_INFO_REQUEST_DATE_PARAMS_MAX_DELTA_IN_DAYS

    @swagger_auto_schema(**swagger.get_financing_sources_info_schema)
    def get(self, request):
        request_serializer = GetFinancingSourcesInfoRequestSerializer(
            data=request.query_params, max_delta_in_days=self.max_date_delta_in_days
        )
        request_serializer.is_valid(raise_exception=True)
        queryset = get_financing_sources_with_count(
            request_serializer.validated_data["from_datetime"], request_serializer.validated_data["to_datetime"]
        )
        response_serializer = GetFinancingSourcesInfoResponseSerializer(queryset, many=True)
        return Response(response_serializer.data)
