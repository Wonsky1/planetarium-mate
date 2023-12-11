from rest_framework import viewsets

from planetarium.models import AstronomyShow, ShowTheme
from planetarium.serializers import AstronomyShowSerializer, AstronomyShowListSerializer, ShowThemeSerializer


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