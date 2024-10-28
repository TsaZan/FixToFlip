from django.test import TestCase

from FixToFlip.properties.models import Property


class PropertyModelTest(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            property_name="Test Property",
            country="Bulgaria",
            town="Sofia",
            address="123 Main Street",
            post_code="1000",
            property_type="AP",
            rooms=3,
            property_size=120,
            bought_date="2023-01-01",
            property_condition="Rp"
        )

    def test_property_creation(self):
        self.assertEqual(self.property.property_name, "Test Property")
        self.assertEqual(self.property.country, "Bulgaria")
        self.assertEqual(self.property.town, "Sofia")
        self.assertEqual(self.property.address, "123 Main Street")
        self.assertEqual(self.property.post_code, "1000")
        self.assertEqual(self.property.property_type, "AP")
        self.assertEqual(self.property.rooms, 3)
        self.assertEqual(self.property.property_size, 120)
        self.assertEqual(self.property.bought_date.format(), "2023-01-01")
        self.assertEqual(self.property.property_condition, "Rp")

    def test_string_representation(self):
        self.assertEqual(str(self.property), "Test Property")

    def test_property_size_positive(self):
        invalid_property = Property(
            property_name="Invalid Property",
            country="Bulgaria",
            town="Sofia",
            address="456 Invalid Street",
            post_code="1000",
            property_type="A",
            rooms=2,
            property_size=-100,
            bought_date="2023-01-01",
            property_condition="Rp"
        )
        with self.assertRaises(Exception):
            invalid_property.full_clean()

    def test_property_condition_choices(self):
        valid_property = Property(
            property_name="Valid Condition Property",
            country="Bulgaria",
            town="Sofia",
            address="789 Valid Street",
            post_code="1000",
            property_type="AP",
            rooms=2,
            property_size=100,
            bought_date="2023-01-01",
            property_condition="Rp"
        )
        valid_property.full_clean()

        invalid_property = Property(
            property_name="Invalid Condition Property",
            country="Bulgaria",
            town="Sofia",
            address="123 Invalid Street",
            post_code="1000",
            property_type="AP",
            rooms=2,
            property_size=100,
            bought_date="2023-01-01",
            property_condition="Z"
        )
        with self.assertRaises(Exception):
            invalid_property.full_clean()
