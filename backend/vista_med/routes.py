from django.urls import include, path
from rest_framework.routers import DefaultRouter

from vista_med.views import (
    EmployeeView,
    GetFinancingSourcesInfoView,
    GetPatientAppointmentsInfo,
    PatientView,
    OrganisationsView,
    OrganisationStructuresView,
)

router = DefaultRouter()
# register ViewSets here

urlpatterns = [
    path("", include(router.urls)),
    path("patient_appointments/", GetPatientAppointmentsInfo.as_view()),
    path("employees/", EmployeeView.as_view()),
    path("patients/", PatientView.as_view()),
    path("financing_sources/", GetFinancingSourcesInfoView.as_view()),
    path("organisations/", OrganisationsView.as_view()),
    path("organisation_structures/", OrganisationStructuresView.as_view()),
]
