from django.urls import path, include
from rest_framework import routers

from planetarium.views import AstronomyShowViewSet, ShowThemeViewSet, PlanetariumDomeViewSet, ShowSessionViewSet

router = routers.DefaultRouter()
router.register("astronomy_shows", AstronomyShowViewSet)
router.register("show_themes", ShowThemeViewSet)
router.register("planetarium_domes", PlanetariumDomeViewSet)
router.register("show_sessions", ShowSessionViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "planetarium"
