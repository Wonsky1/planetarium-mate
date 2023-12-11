from rest_framework import viewsets

from django.db.models import F, Count

from planetarium.models import AstronomyShow, ShowTheme, PlanetariumDome, ShowSession
from planetarium.serializers import AstronomyShowSerializer, AstronomyShowListSerializer, ShowThemeSerializer, \
    PlanetariumDomeSerializer, ShowSessionSerializer, ShowSessionListSerializer


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.prefetch_related("themes")
    serializer_class = AstronomyShowSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer
        return AstronomyShowSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = (
        ShowSession.objects
        .select_related("astronomy_show", "planetarium_dome")
        .annotate(
            tickets_available=(
            F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row")
            - Count("tickets")
            )
        )
    )
    serializer_class = ShowSessionSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        return ShowSessionSerializer