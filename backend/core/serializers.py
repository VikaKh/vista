from django.conf import settings
from django.contrib.auth.password_validation import validate_password as validate_password_django
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from core.models import User, Review, OrganizationGis
from vista_med.models import Organisation
from vista_med.serializers import OrganisationSerializer


class RegisterRequestSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    patronymic = serializers.CharField(max_length=150, required=False)

    def validate_password(self, password):
        validate_password_django(password)
        return password

    def create(self, data):
        return User.objects.create_user(**data)

    class Meta:
        model = User
        fields = ["first_name", "patronymic", "last_name", "username", "password"]


class AuthResponseSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source="get_auth_token")
    organisation = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=OrganisationSerializer)
    def get_organisation(self, instance):
        org = Organisation.objects.filter(id=settings.DEFAULT_ORG_ID).first()
        return OrganisationSerializer(org).data if org else None

    class Meta:
        model = User
        fields = ["first_name", "patronymic", "last_name", "token", "organisation"]


class OrganizationGisSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationGis
        fields = ["org_name", "gis_id"]


class ReviewSerializer(serializers.ModelSerializer):
    gis_org = OrganizationGisSerializer()

    class Meta:
        model = Review
        fields = ["text", "rating", "user_name", "gis_org"]
