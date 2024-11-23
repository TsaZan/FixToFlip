from django.test import TestCase

from django.contrib.auth import get_user_model

User = get_user_model()


class BaseAccountManagerTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username="testuser", password="password123")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("password123"))

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(username="admin", password="admin123")
        self.assertEqual(superuser.username, "admin")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
