from datetime import timedelta
from types import SimpleNamespace
from typing import Optional

from rest_framework import serializers

from .models import Action, Employee, FinancingSource, Organisation, OrganisationStructure, Patient
from .services import AppointmentStatus, AppointmentStatusReturnedInInfo

ZERO_TIMEDELTA = timedelta()


class PatientAppointmentsInfoGetRequestParamSerializer(serializers.Serializer):
    status = serializers.ChoiceField([e.value for e in AppointmentStatus], default=AppointmentStatus.ANY.value)
    from_datetime = serializers.DateTimeField(required=False, help_text="Mutually exclusive with from_date and to_date")
    to_datetime = serializers.DateTimeField(required=False, help_text="Mutually exclusive with from_date and to_date")
    from_date = serializers.DateField(
        required=False,
        help_text=(
            "Mutually exclusive with from_datetime and to_datetime."
            "If equals to to_date, appointments for this single day will be returned."
        ),
    )
    to_date = serializers.DateField(
        required=False,
        help_text=(
            "Mutually exclusive with from_datetime and to_datetime."
            "If equals to to_date, appointments for this single day will be returned."
        ),
    )
    patient = serializers.IntegerField(required=False, help_text="patient id")
    employee = serializers.IntegerField(required=False, help_text="executing employee id")
    organisation = serializers.IntegerField(required=False, help_text="executing employee's organisation id")
    organisation_structure = serializers.IntegerField(required=False, help_text="executing employee's organisation structure id")

    def __init__(self, *args, max_date_delta_in_days: Optional[int] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_date_delta_in_days = max_date_delta_in_days
        self._max_timedelta = None if max_date_delta_in_days is None else timedelta(days=max_date_delta_in_days)

    def to_internal_value(self, data):
        if self.max_date_delta_in_days is not None and all(
            key not in data for key in ("from_datetime", "to_datetime", "from_date", "to_date")
        ):
            err_msg = "необходимо передать хотя бы одну из границ диапазона дат"
            raise serializers.ValidationError({"from_datetime, to_datetime, from_date, to_date": err_msg})

        mutually_exclusive_params = []
        if (a := "from_date") in data:
            if (b := "from_datetime") in data:
                mutually_exclusive_params.append((a, b))
            if (b := "to_datetime") in data:
                mutually_exclusive_params.append((a, b))
        if (a := "to_date") in data:
            if (b := "to_datetime") in data:
                mutually_exclusive_params.append((a, b))
            if (b := "from_datetime") in data:
                mutually_exclusive_params.append((b, a))
        if mutually_exclusive_params:
            field_errors = {}
            for pair in mutually_exclusive_params:
                field_errors[", ".join(pair)] = "эти параметры взаимоисключающие"
            raise serializers.ValidationError(field_errors)

        validated_data = super().to_internal_value(data)
        from_dt = validated_data.get(a := "from_datetime") or validated_data.get(a := "from_date")
        to_dt = validated_data.get(b := "to_datetime") or validated_data.get(b := "to_date")
        if from_dt is not None and to_dt is not None:
            dt_delta = to_dt - from_dt
            err_msg = "разница дат должна быть => 0"
            if self.max_date_delta_in_days is not None:
                err_msg += f" and <= {self.max_date_delta_in_days}"
            if dt_delta < ZERO_TIMEDELTA:
                raise serializers.ValidationError({f"{b}, {a}": err_msg})
            if self.max_date_delta_in_days is not None and dt_delta > self._max_timedelta:
                raise serializers.ValidationError({f"{b}, {a}": err_msg})

        return validated_data


class AppointmentInfoPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id", "last_name", "first_name", "patr_name")


class AppointmentInfoEmployeeOrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ("id", "full_name")


class AppointmentInfoEmployeeOrganisationStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationStructure
        fields = ("id", "name", "organisation")


class AppointmentInfoEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "last_name", "first_name", "patr_name", "organisation", "organisation_structure")

    organisation = AppointmentInfoEmployeeOrganisationSerializer()
    organisation_structure = AppointmentInfoEmployeeOrganisationStructureSerializer()


class PatientAppointmentsInfoGetRequestResponseSerializer(serializers.Serializer):
    type = serializers.SlugRelatedField(slug_field="name", read_only=True, source="event.type")
    status = serializers.ChoiceField([e.value for e in AppointmentStatusReturnedInInfo])
    start_at = serializers.SlugRelatedField(slug_field="start_at", read_only=True, source="event")
    patient = AppointmentInfoPatientSerializer()
    employee = AppointmentInfoEmployeeSerializer()

    def to_representation(self, instance: Action):
        appointment_info = SimpleNamespace(
            status=instance.status,
            event=instance.event,
            patient=instance.event.patient,
            employee=instance.executing_employee,
        )
        return super().to_representation(appointment_info)


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ["id", "full_name"]


class OrganisationStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationStructure
        fields = ["id", "name"]


class EmployeeSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer(read_only=True)
    organisation_structure = OrganisationStructureSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "last_name", "first_name", "patr_name", "organisation", "organisation_structure"]


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "last_name", "first_name", "patr_name", "birth_date"]


class GetFinancingSourcesInfoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancingSource
        fields = ["id", "name", "total_count"]

    total_count = serializers.IntegerField()


class GetFinancingSourcesInfoRequestSerializer(serializers.Serializer):
    from_datetime = serializers.DateTimeField()
    to_datetime = serializers.DateTimeField()

    def __init__(self, instance=None, data=..., max_delta_in_days=None, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self.max_delta = timedelta(days=max_delta_in_days) if max_delta_in_days else timedelta.max

    def validate(self, data):
        delta = data["to_datetime"] - data["from_datetime"]
        if delta < ZERO_TIMEDELTA or delta > self.max_delta:
            raise serializers.ValidationError(
                {"from_datetime, to_datetime": f"Разница дат должна быть >= 0 и <= {self.max_delta.days} дней."}
            )
        return data
