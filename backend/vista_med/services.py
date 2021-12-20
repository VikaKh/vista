from collections import defaultdict
from datetime import date, datetime
from enum import Enum
from typing import Literal, Optional, Union

from django.db.models import Case, Count, Exists, FilteredRelation, OuterRef, Q, Value, When
from django.utils.timezone import now

from .models import Action, Employee, FinancingSource, Patient, Organisation, OrganisationStructure, Visit


class EventTypeName(Enum):
    PATIENT_APPOINTMENT = "Запись на прием"


class ActionTypeName(Enum):
    PATIENT_APPOINTMENT = "запись на прием"


class AppointmentStatus(Enum):
    ANY = "any"
    SCHEDULED = "scheduled"
    VISITED = "visited"
    MISSED = "missed"


class AppointmentStatusReturnedInInfo(Enum):
    SCHEDULED = "scheduled"
    VISITED = "visited"
    MISSED = "missed"


AppointmentStatusLiteral = Literal["any", "scheduled", "visited", "missed"]

OptionalDatetimeOrDate = Optional[Union[datetime, date]]


def _get_base_patient_appointments_queryset(
    from_dt: OptionalDatetimeOrDate = None,
    to_dt: OptionalDatetimeOrDate = None,
    executing_employee: Employee = None,
    patient: Patient = None,
    organisation: Organisation = None,
    organisation_structure: OrganisationStructure = None,
):
    date_params = []
    if from_dt is not None:
        if isinstance(from_dt, datetime):
            q = Q(direction_date__gte=from_dt)
        elif isinstance(from_dt, date):
            q = Q(direction_date__date__gte=from_dt)
        else:
            raise TypeError(f"`from_dt` must be either of type {datetime} or {date}, not {type(from_dt)}")
        date_params.append(q)
    if to_dt is not None:
        if isinstance(to_dt, datetime):
            q = Q(direction_date__lte=to_dt)
        elif isinstance(to_dt, date):
            q = Q(direction_date__date__lte=to_dt)
        else:
            raise TypeError(f"`to_dt` must be either of type {datetime} or {date}, not {type(to_dt)}")
        date_params.append(q)
    qs = Action.objects.select_related(
        "event",
        "event__type",
        "event__patient",
        "executing_employee",
        "executing_employee__organisation",
        "executing_employee__organisation_structure",
    ).filter(type__name=ActionTypeName.PATIENT_APPOINTMENT.value, *date_params)
    if executing_employee is not None:
        qs = qs.filter(executing_employee=executing_employee)
    elif organisation_structure is not None:
        qs = qs.filter(executing_employee__organisation_structure=organisation_structure)
    elif organisation is not None:
        qs = qs.filter(executing_employee__organisation=organisation)
    if patient is not None:
        qs = qs.filter(event__patient=patient)
    return qs.order_by("direction_date")


def get_patient_appointments_for_period(
    status: Union[AppointmentStatus, AppointmentStatusLiteral],
    from_dt: OptionalDatetimeOrDate = None,
    to_dt: OptionalDatetimeOrDate = None,
    executing_employee: Employee = None,
    patient: Patient = None,
    organisation: Organisation = None,
    organisation_structure: OrganisationStructure = None,
):
    base_qs = _get_base_patient_appointments_queryset(
        from_dt, to_dt, executing_employee, patient, organisation, organisation_structure
    ).annotate(
        status=Case(
            When(
                Exists(
                    Action.objects.filter(event=OuterRef("event")).exclude(
                        type__name=ActionTypeName.PATIENT_APPOINTMENT.value
                    )
                ),
                then=Value(AppointmentStatusReturnedInInfo.VISITED.value),
            ),
            When(direction_date__lt=now(), then=Value(AppointmentStatusReturnedInInfo.MISSED.value)),
            default=Value(AppointmentStatusReturnedInInfo.SCHEDULED.value),
        )
    )
    status = AppointmentStatus(status)
    if status is AppointmentStatus.ANY:
        return base_qs
    elif status is AppointmentStatus.SCHEDULED:
        return base_qs.filter(status=AppointmentStatusReturnedInInfo.SCHEDULED.value)
    elif status is AppointmentStatus.VISITED:
        return base_qs.filter(status=AppointmentStatusReturnedInInfo.VISITED.value)
    elif status is AppointmentStatus.MISSED:
        return base_qs.filter(status=AppointmentStatusReturnedInInfo.MISSED.value)
    else:
        raise ValueError(f"unknown {AppointmentStatus} member: {status}")


def get_financing_sources_with_count(from_datetime, to_datetime):
    actions = Action.objects.filter(direction_date__gte=from_datetime, direction_date__lte=to_datetime).values_list(
        "financing_source_id", flat=True
    )
    visits = Visit.objects.filter(direction_date__gte=from_datetime, direction_date__lte=to_datetime).values_list(
        "financing_source_id", flat=True
    )
    counts = defaultdict(int)
    for action_financing_source_id in actions:
        counts[action_financing_source_id] += 1
    for visit_financing_source_id in visits:
        counts[visit_financing_source_id] += 1
    financing_sources = FinancingSource.objects.all()
    for financing_source in financing_sources:
        financing_source.total_count = counts[financing_source.id]
    return [financing_source for financing_source in financing_sources if financing_source.total_count > 0]
