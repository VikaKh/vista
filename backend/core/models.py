from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    patronymic = models.CharField(max_length=150, blank=True)

    def get_auth_token(self):
        return Token.objects.get_or_create(user=self)[0]


class OrganizationGis(models.Model):
    org_name = models.CharField(max_length=150)
    gis_id = models.BigIntegerField()


class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField()
    user_name = models.CharField(max_length=100)
    gis_org = models.ForeignKey(OrganizationGis, on_delete=models.CASCADE)
