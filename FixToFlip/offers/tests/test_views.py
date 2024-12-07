from django.test import TestCase, Client
from django.urls import reverse

from FixToFlip.offers.models import Offer
from FixToFlip.properties.models import Property
from django.contrib.auth import get_user_model

User = get_user_model()


class DashboardOffersViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.property = Property.objects.create(
            property_name="Test Property",
            owner=self.user
        )
        Offer.objects.create(
            title="Test Offer",
            listed_property=self.property,
            offer_status="Active",
        )
        self.url = reverse('offers_main_page')

    def test_dashboard_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offers-list.html')


class AddOfferViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.property = Property.objects.create(
            property_name="Test Property",
            owner=self.user
        )
        self.url = reverse('create_offer', kwargs={'pk': self.property.pk})

    def test_add_offer_view_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/add-offer.html')

    def test_add_offer_view_post_valid(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'New Test Offer',
            'description': 'Description for new test offer.',
            'listed_price_0': '100000',
            'listed_price_1': 'EUR',
            'offer_status': 'Active',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Offer.objects.filter(title='New Test Offer').exists())


class EditOfferViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.property = Property.objects.create(
            property_name="Test Property",
            owner=self.user
        )
        self.offer = Offer.objects.create(
            title="Test Offer",
            listed_property=self.property,
            offer_status="Active",
        )
        self.url = reverse('edit_offer', kwargs={'pk': self.offer.pk})

    def test_edit_offer_view_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/edit-offer.html')

    def test_edit_offer_view_post_valid(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'Updated Test Offer',
            'description': 'Updated description.',
            'listed_price_0': '150000',
            'listed_price_1': 'EUR',
            'offer_status': 'Sold',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.title, 'Updated Test Offer')
        self.assertEqual(self.offer.offer_status, 'Sold')


class OfferDeleteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.property = Property.objects.create(
            property_name="Test Property",
            owner=self.user
        )
        self.offer = Offer.objects.create(
            title="Test Offer",
            listed_property=self.property,
            offer_status="Active",
        )
        self.url = reverse('delete_offer', kwargs={'pk': self.offer.pk})

    def test_delete_offer_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Offer.objects.filter(pk=self.offer.pk).exists())


class OfferAPIViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.property = Property.objects.create(
            property_name="Test Property",
            owner=self.user
        )
        self.offer = Offer.objects.create(
            title="Test Offer",
            listed_property=self.property,
            offer_status="Active",
        )
        self.url = reverse('detail_offer', kwargs={'pk': self.offer.pk})
        print(self.url)

    def test_offer_api_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Test Offer')
