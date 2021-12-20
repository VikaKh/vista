import django
import os

# all imports from core should go after django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_clinic.settings")
django.setup()
import requests

from core.models import Review, OrganizationGis


def get_reviews():
    gis_orgs_list = OrganizationGis.objects.values("id", "gis_id")
    for gis_org in gis_orgs_list:
        gis_id = gis_org["gis_id"]
        response = requests.get(
            f"https://public-api.reviews.2gis.com/2.0/branches/{gis_id}/reviews",
            params={
                "limit": "50",
                "is_advertiser": "true",
                "fields": "reviews.hiding_reason",
                "without_my_first_review": "false",
                "rated": "true",
                "sort_by": "date_edited",
                "key": "37c04fe6-a560-4549-b459-02309cf643ad",
                "locale": "ru_RU",
            },
        )
        reviews_list = response.json()["reviews"]
        for review in reviews_list:
            Review.objects.get_or_create(
                text=review["text"], rating=review["rating"], user_name=review["user"]["name"], gis_org_id=gis_org["id"]
            )


get_reviews()
