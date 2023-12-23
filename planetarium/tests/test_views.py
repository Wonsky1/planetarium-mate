from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from datetime import datetime
from planetarium.models import (
    PlanetariumDome,
    ShowTheme,
    AstronomyShow,
    ShowSession,
    Reservation
)


def sample_admin():
    return get_user_model().objects.create_user(
        email='admin@gmail.com', password='admin', is_staff=True
    )


def sample_user():
    return get_user_model().objects.create_user(
        email="test@gmail.com", password="test"
    )


class PlanetariumDomeViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.planetarium_dome_url = reverse('planetarium:planetariumdome-list')
        self.admin_user = sample_admin()
        self.client.force_authenticate(user=self.admin_user)

    def test_list_planetarium_domes(self):
        response = self.client.get(self.planetarium_dome_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create_planetarium_dome_fail(self):
        client = APIClient()
        user = sample_user()
        client.force_authenticate(user=user)
        data = {'name': 'Test Dome', 'rows': 5, "seats_in_row": 5}

        response = client.post(self.planetarium_dome_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_planetarium_dome_success(self):
        data = {'name': 'Test Dome', 'rows': 5, "seats_in_row": 5}
        response = self.client.post(self.planetarium_dome_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PlanetariumDome.objects.count(), 1)
        self.assertEqual(PlanetariumDome.objects.get().name, 'Test Dome')


class ShowThemeViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.show_theme_url = reverse('planetarium:showtheme-list')
        self.admin_user = sample_admin()
        self.client.force_authenticate(user=self.admin_user)

    def test_list_show_themes(self):
        response = self.client.get(self.show_theme_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create_show_theme_fail(self):
        client = APIClient()
        user = sample_user()
        client.force_authenticate(user=user)
        data = {'name': 'Test Theme'}

        response = client.post(self.show_theme_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_show_theme_success(self):
        data = {'name': 'Test Theme'}
        response = self.client.post(self.show_theme_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShowTheme.objects.count(), 1)
        self.assertEqual(ShowTheme.objects.get().name, 'Test Theme')


class AstronomyShowViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.astronomy_show_url = reverse('planetarium:astronomyshow-list')
        self.admin_user = sample_admin()
        self.client.force_authenticate(user=self.admin_user)

    def test_list_astronomy_shows(self):
        response = self.client.get(self.astronomy_show_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ShowSessionViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.show_session_url = reverse('planetarium:showsession-list')
        self.admin_user = sample_admin()
        self.client.force_authenticate(user=self.admin_user)

    def test_list_show_sessions(self):
        response = self.client.get(self.show_session_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_show_session(self):
        show_theme = ShowTheme.objects.create(name="Test Theme")
        astronomy_show_data = {'title': 'Test Show', 'description': 'Test Description'}
        astronomy_show = AstronomyShow.objects.create(**astronomy_show_data)
        astronomy_show.themes.set([show_theme.id])
        planetarium_dome = PlanetariumDome.objects.create(seats_in_row=5, rows=5, name="Test Dome")
        data = {'astronomy_show': '1', 'planetarium_dome': '1', "show_time": datetime.now()}
        response = self.client.post(self.show_session_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShowSession.objects.count(), 1)
        self.assertEqual(ShowSession.objects.get(id=1).astronomy_show.title, 'Test Show')


class ReservationViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.reservation_url = reverse('planetarium:reservation-list')
        self.show_theme = ShowTheme.objects.create(name="Test Theme")
        self.astronomy_show = AstronomyShow.objects.create(title="Test", description="Test")
        self.astronomy_show.themes.set([self.show_theme.id])
        self.planetarium_dome = PlanetariumDome.objects.create(seats_in_row=5, rows=5, name="Test Dome")
        self.data = {'astronomy_show': '1', 'planetarium_dome': '1', "show_time": datetime.now()}
        self.show_session = ShowSession.objects.create(
            astronomy_show=self.astronomy_show,
            planetarium_dome=self.planetarium_dome,
            show_time=datetime.now()
        )
        self.user = sample_user()
        self.client.force_authenticate(user=self.user)

    def test_list_reservations(self):
        response = self.client.get(self.reservation_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_reservation(self):
        data = {"tickets": [{"row": 5, "seat": 5, "show_session": 1}, ]}
        response = self.client.post(self.reservation_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.get().user, self.user)

    def test_create_reservation_unauthenticated_fail(self):
        client = APIClient()
        response = client.post(self.reservation_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
