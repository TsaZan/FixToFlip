from django.test import TestCase
from djmoney.money import Money

from FixToFlip.choices import PublishChoices
from FixToFlip.offers.models import Offer
from FixToFlip.properties.models import Property
from datetime import date

from django.contrib.auth import get_user_model

User = get_user_model()


class OfferModelTest(TestCase):

    def setUp(self):
        self.property = Property.objects.create(
            property_name="Test Property",
            country="Test Country",
            city="Test Town",
            address="123 Test St",
            property_type="House",
            bedrooms=3,
            property_size=120,
            bought_date="2023-01-01",
            property_condition="New",
            owner=User.objects.create_user(
                username='testuser',
                password='testpassword'
            ),
        )

        self.offer = Offer.objects.create(
            title="Test Offer",
            description="Test description for offer.",
            listed_price=Money(100000, "EUR"),
            offer_status="Active",
            listed_property=self.property,
            actual_sold_price=Money(95000, "EUR"),
            sold_date=date(2023, 10, 5),
            is_published=True,
        )

    def test_offer_creation(self):
        self.assertEqual(self.offer.title, "Test Offer")
        self.assertEqual(self.offer.description, "Test description for offer.")
        self.assertEqual(self.offer.listed_price.amount, 100000)
        self.assertEqual(str(self.offer.listed_price.currency), "EUR")
        self.assertEqual(self.offer.actual_sold_price.amount, 95000)
        self.assertEqual(str(self.offer.actual_sold_price.currency), "EUR")
        self.assertEqual(self.offer.offer_status, "Active")
        self.assertTrue(self.offer.is_published)
        self.assertEqual(self.offer.listed_property, self.property)

    def test_offer_string_representation(self):
        self.assertEqual(str(self.offer), "Test Offer")

    def test_offer_default_values(self):
        new_offer = Offer.objects.create(
            title="Default Test Offer",
            description="Default description.",
        )
        self.assertEqual(new_offer.listed_price.amount, 0)
        self.assertEqual(str(new_offer.listed_price.currency), "EUR")
        self.assertEqual(new_offer.is_published, PublishChoices.NO)
        self.assertIsNone(new_offer.listed_property)
        self.assertIsNone(new_offer.sold_date)

    def test_ordering(self):
        second_offer = Offer.objects.create(
            title="Another Test Offer",
            description="Second description.",
        )
        offers = Offer.objects.all()
        self.assertEqual(offers.first(), second_offer)
        self.assertEqual(offers.last(), self.offer)


