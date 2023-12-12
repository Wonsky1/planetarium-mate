from datetime import datetime

from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from django.db.models import F, Count

from planetarium.models import (
    AstronomyShow,
    ShowTheme,
    PlanetariumDome,
    ShowSession,
    Reservation
)
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly
from planetarium.serializers import (
    AstronomyShowSerializer,
    AstronomyShowListSerializer,
    ShowThemeSerializer,
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    ShowSessionListSerializer,
    ReservationSerializer,
    ReservationListSerializer, AstronomyShowImageSerializer, AstronomyShowDetailSerializer
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly, ]


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.prefetch_related("themes")
    serializer_class = AstronomyShowSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly, ]

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        title = self.request.query_params.get("title")
        themes = self.request.query_params.get("themes")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if themes:
            themes_ids = self._params_to_ints(themes)
            queryset = queryset.filter(themes__id__in=themes_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer
        if self.action == "retrieve":
            return AstronomyShowDetailSerializer
        if self.action == "upload_image":
            return AstronomyShowImageSerializer
        return AstronomyShowSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific movie"""
        movie = self.get_object()
        serializer = self.get_serializer(movie, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "themes",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by themes id (ex. ?themes=2,5)",
            ),
            OpenApiParameter(
                "title",
                type=OpenApiTypes.STR,
                description="Filter by show title (ex. ?title=earth)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly, ]


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = (
        ShowSession.objects
        .select_related("astronomy_show", "planetarium_dome")
        .annotate(
            tickets_available=(
                F("planetarium_dome__rows")
                * F("planetarium_dome__seats_in_row")
                - Count("tickets")
            )
        )
    )
    serializer_class = ShowSessionSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly, ]

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        return ShowSessionSerializer

    def get_queryset(self):
        date = self.request.query_params.get("date")
        show_id_str = self.request.query_params.get("show")

        queryset = self.queryset

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if show_id_str:
            queryset = queryset.filter(astronomy_show_id=int(show_id_str))

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "show",
                type=OpenApiTypes.INT,
                description="Filter by show id (ex. ?show=2)",
            ),
            OpenApiParameter(
                "date",
                type=OpenApiTypes.DATE,
                description=(
                    "Filter by datetime of Show Session "
                    "(ex. ?date=2022-10-23)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReservationPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Reservation.objects.prefetch_related(
        "tickets__show_session__astronomy_show",
        "tickets__show_session__planetarium_dome"
    )
    serializer_class = ReservationSerializer
    pagination_class = ReservationPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
