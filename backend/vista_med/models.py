from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True
        managed = False


class ActionType(BaseModel):
    name = models.CharField(max_length=512, db_column="name")

    class Meta(BaseModel.Meta):
        db_table = "ActionType"


class EventType(BaseModel):
    name = models.CharField(max_length=64, db_column="name")

    class Meta(BaseModel.Meta):
        db_table = "EventType"


class FinancingSource(BaseModel):
    name = models.CharField(max_length=64, db_column="name")

    class Meta(BaseModel.Meta):
        db_table = "rbFinance"


class Organisation(BaseModel):
    full_name = models.CharField(max_length=636, db_column="fullName")

    class Meta(BaseModel.Meta):
        db_table = "Organisation"


class OrganisationStructure(BaseModel):
    name = models.CharField(max_length=256, db_column="name")
    organisation = models.ForeignKey(
        Organisation, models.DO_NOTHING, related_name="structures", db_column="organisation_id"
    )

    class Meta(BaseModel.Meta):
        db_table = "OrgStructure"


class Employee(BaseModel):
    first_name = models.CharField(max_length=30, db_column="firstName")
    patr_name = models.CharField(max_length=30, db_column="patrName")
    last_name = models.CharField(max_length=120, db_column="lastName")
    organisation = models.ForeignKey(Organisation, models.DO_NOTHING, related_name="employees", db_column="org_id")
    organisation_structure = models.ForeignKey(
        OrganisationStructure, models.DO_NOTHING, related_name="employees", db_column="orgStructure_id"
    )

    class Meta(BaseModel.Meta):
        db_table = "Person"


class Patient(BaseModel):
    first_name = models.CharField(max_length=30, db_column="firstName")
    patr_name = models.CharField(max_length=64, db_column="patrName")
    last_name = models.CharField(max_length=30, db_column="lastName")
    birth_date = models.DateField(db_column="birthDate")

    class Meta(BaseModel.Meta):
        db_table = "Client"


class Event(BaseModel):
    type = models.ForeignKey(EventType, models.DO_NOTHING, related_name="events", db_column="eventType_id")
    start_at = models.DateTimeField(db_column="setDate")
    executed_at = models.DateTimeField(db_column="execDate")
    patient = models.ForeignKey(Patient, models.DO_NOTHING, related_name="events", db_column="client_id")
    employee_who_set = models.ForeignKey(
        Employee, models.DO_NOTHING, related_name="events_set_by", db_column="setPerson_id"
    )

    class Meta(BaseModel.Meta):
        db_table = "Event"


class Action(BaseModel):
    type = models.ForeignKey(ActionType, models.DO_NOTHING, related_name="actions", db_column="actionType_id")
    direction_date = models.DateTimeField(db_column="directionDate")
    start_at = models.DateTimeField(db_column="begDate")
    executed_at = models.DateTimeField(db_column="endDate")
    event = models.ForeignKey(Event, models.DO_NOTHING, related_name="actions", db_column="event_id")
    executing_employee = models.ForeignKey(Employee, models.DO_NOTHING, related_name="actions", db_column="person_id")
    financing_source = models.ForeignKey(
        FinancingSource, models.DO_NOTHING, related_name="actions", db_column="finance_id"
    )

    class Meta(BaseModel.Meta):
        db_table = "Action"


class Visit(BaseModel):
    event = models.ForeignKey(Event, models.DO_NOTHING, related_name="visits", db_column="event_id")
    executing_employee = models.ForeignKey(Employee, models.DO_NOTHING, related_name="visits", db_column="person_id")
    financing_source = models.ForeignKey(
        FinancingSource, models.DO_NOTHING, related_name="visits", db_column="finance_id"
    )
    direction_date = models.DateTimeField(db_column="date")

    class Meta(BaseModel.Meta):
        db_table = "Visit"
