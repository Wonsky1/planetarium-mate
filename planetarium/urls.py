from django.urls import path, include
from rest_framework import routers

from planetarium.views import AstronomyShowViewSet, ShowThemeViewSet

router = routers.DefaultRouter()
router.register("astronomy_shows", AstronomyShowViewSet)
router.register("show_themes", ShowThemeViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "planetarium"
