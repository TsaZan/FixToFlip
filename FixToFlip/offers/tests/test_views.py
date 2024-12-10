from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase

from FixToFlip.accounts.models import BaseAccount, Profile
from FixToFlip.offers.models import Offer
from FixToFlip.offers.serializers import OfferAPISerializer
from FixToFlip.properties.models import Property
from django.contrib.auth import get_user_model

User = get_user_model()


class DashboardOffersViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.property = Property.objects.create(
            property_name="Test Property", owner=self.user
        )
        Offer.objects.create(
            title="Test Offer",
            listed_property=self.property,
            offer_status="Active",
        )
        self.url = reverse("offers_main_page")

    def test_dashboard_view_authenticated(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "offers/offers-list.html")


class AddOfferViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.property = Property.objects.create(
            property_name="Test Property", owner=self.user
        )
        self.url = reverse("create_offer", kwargs={"pk": self.property.pk})

    def test_add_offer_view_get(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "offers/add-offer.html")

    def test_add_offer_view_post_valid(self):
        self.client.login(username="testuser", password="testpass")
        data = {
            "title": "New Test Offer For Add Offer View Test",
            "description": "Description for new test offer for add offer view test.",
            "listed_price_0": "100000",
            "listed_price_1": "EUR",
            "offer_status": "Active",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Offer.objects.filter(
                title="New Test Offer For Add Offer View Test"
            ).exists()
        )


class OfferDeleteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.property = Property.objects.create(
            property_name="Test Property", owner=self.user
        )
        self.offer = Offer.objects.create(
            title="Test Offer",
            listed_property=self.property,
            offer_status="Active",
        )
        self.url = reverse("delete_offer", kwargs={"pk": self.offer.pk})

    def test_delete_offer_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Offer.objects.filter(pk=self.offer.pk).exists())


class OfferAPISerializerTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com")
        self.profile, created = Profile.objects.get_or_create(
            user=self.user,
            defaults={
                "profile_type": "Personal",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "123456789",
            },
        )

        self.property = Property.objects.create(
            country="Country",
            city="City",
            address="123 Test St",
            property_type="Apartment",
            year_of_built=2020,
            property_size=100,
            floor=2,
            bedrooms=3,
            bathrooms=2,
            owner=self.user,
        )

        self.offer = Offer.objects.create(
            title="Test Offer",
            description="A great offer",
            listed_price=100000,
            listed_price_currency="EUR",
            offer_status="Active",
            listed_property=self.property,
        )

    def test_offer_serialization(self):
        serializer = OfferAPISerializer(instance=self.offer)
        data = serializer.data
        self.assertEqual(data["id"], self.offer.id)
        self.assertEqual(data["title"], "Test Offer")
        self.assertEqual(data["description"], "A great offer")
        self.assertEqual(data["listed_price"], "100000.00")
        self.assertEqual(data["listed_price_currency"], "EUR")
        self.assertEqual(data["offer_status"], "Active")
        self.assertEqual(data["listed_property"]["city"], "City")
