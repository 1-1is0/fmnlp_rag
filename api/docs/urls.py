from rest_framework import routers
from docs.views import DocumentViewSet
from django.urls import path, include

app_name = "docs"
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"docs", DocumentViewSet, basename="DocumentViewSet")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
]