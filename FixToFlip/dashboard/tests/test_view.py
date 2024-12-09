from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from FixToFlip.properties.models import Property

User = get_user_model()


class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = reverse('index')

        Property.objects.create(property_name='Property 1', owner=self.user, property_condition='Under repair')
        Property.objects.create(property_name='Property 2', owner=self.user, property_condition='For sale')
        Property.objects.create(property_name='Property 3', owner=self.user, property_condition='Sold')

        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        Property.objects.create(property_name='Property 4', owner=other_user, property_condition='For sale')

        self.dashboard_url = reverse('dashboard')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, f"{self.login_url}?next={self.dashboard_url}")

    def test_view_with_logged_in_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard-index.html')

        # Check context data
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['header_title'], 'Dashboard')
        self.assertQuerySetEqual(
            response.context['all_properties'],
            Property.objects.filter(owner=self.user),
            transform=lambda x: x
        )
        self.assertQuerySetEqual(
            response.context['properties_in_repair'],
            Property.objects.filter(owner=self.user, property_condition='Under repair'),
            transform=lambda x: x
        )
        self.assertQuerySetEqual(
            response.context['repaired_properties'],
            Property.objects.filter(owner=self.user, property_condition='Repaired'),
            transform=lambda x: x
        )
        self.assertQuerySetEqual(
            response.context['properties_sold'],
            Property.objects.filter(owner=self.user, property_condition='Sold'),
            transform=lambda x: x
        )
