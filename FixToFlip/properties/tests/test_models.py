from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from FixToFlip.properties.models import Property

User = get_user_model()


class PropertyModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        if not User.objects.filter(username="testuser").exists():
            self.user = User.objects.create_user(
                username="testuser",
                email="testuser@example.com",
                password="testpassword123",
            )
        else:
            self.user = User.objects.get(username="testuser")

        self.client = Client()
        self.property = Property.objects.create(
            property_name="Test Property",
            country="Bulgaria",
            city="Sofia",
            address="123 Main Street",
            property_type="Residential",
            bedrooms=3,
            bathrooms=2,
            floor=1,
            year_of_built=2005,
            property_size=120,
            bought_date="2023-01-01",
            notes="No additional notes.",
            property_condition="Sold",
            owner=self.user,
        )

    def property_name_max_length_test(self):
        property = Property.objects.get(id=self.property.id)
        max_length = property._meta.get_field("property_name").max_length
        self.assertEqual(max_length, 100)

    def bought_date_test(self):
        self.assertEqual(self.property.bought_date, "2023-01-01")

    def property_str_test(self):
        self.assertEqual(str(self.property), "Test Property")

    def property_owner_test(self):
        self.assertEqual(self.property.owner, self.user)

    def properties_filter_test(self):
        properties = Property.objects.filter(property_condition="Sold")
        self.assertIn(self.property, properties)

    def dates_test(self):
        self.assertIsNotNone(self.property.created_at)
        self.assertIsNotNone(self.property.updated_at)

    def property_size_test(self):
        self.assertEqual(self.property.property_size, 120)
