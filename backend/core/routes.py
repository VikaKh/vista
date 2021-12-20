from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import Login, Register, ReviewView

router = DefaultRouter()
# register ViewSets here

urlpatterns = [
    path("", include(router.urls)),
    path("login/", Login.as_view()),
    path("register/", Register.as_view()),
    path("reviews/", ReviewView.as_view()),
]
