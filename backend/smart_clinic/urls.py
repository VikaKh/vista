from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(title="Smart Clinic", default_version="v1"), permission_classes=(AllowAny,), public=True
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.routes")),
    path("api/", include("vista_med.routes")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
