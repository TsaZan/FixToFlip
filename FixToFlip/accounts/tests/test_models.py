from django.test import TestCase
from django.core.exceptions import ValidationError
from FixToFlip.accounts.models import BaseAccount
from FixToFlip.choices import UserRoles


class AccountsModelTests(TestCase):

    def setUp(self):
        self.account1 = BaseAccount.objects.create(
            role='investor',
            username='user1',
            email='user1@fixtoflip.com',
            first_name='First',
            last_name='Last'
        )

    def test_username_unique(self):
        with self.assertRaises(ValidationError):
            account2 = BaseAccount(
                role='broker',
                username=self.account1.username,
                email='user2@fixtoflip.com',
                first_name='New',
                last_name='User'
            )
            account2.full_clean()

    def test_email_unique(self):
        with self.assertRaises(ValidationError):
            account3 = BaseAccount(
                role='investor',
                username='user3',
                email=self.account1.email,
                first_name='Another',
                last_name='User'
            )
            account3.full_clean()

    def test_role_choices(self):
        account_investor = BaseAccount(role=UserRoles.INVESTOR, username='testuser1', email='investor@fixtoflip.com',
                                       first_name='Investor', last_name='User')
        account_investor.full_clean()

        account_broker = BaseAccount(role=UserRoles.BROKER, username='testuser2', email='broker@fixtoflip.com',
                                     first_name='Broker', last_name='User')
        account_broker.full_clean()

        self.assertEqual(account_investor.role, UserRoles.INVESTOR)
        self.assertEqual(account_broker.role, UserRoles.BROKER)

    def test_invalid_role(self):
        with self.assertRaises(ValidationError):
            account_invalid = BaseAccount(role='invalid_role', username='testuser3', email='invalid@fixtoflip.com',
                                          first_name='Invalid', last_name='User')
            account_invalid.full_clean()

    def test_date_fields(self):
        self.assertIsNotNone(self.account1.date_joined)
        self.assertIsNotNone(self.account1.last_login)
        self.assertIsNotNone(self.account1.updated_at)
        self.assertIsNotNone(self.account1.last_activity)

    def test_string_representation(self):
        self.assertEqual(str(self.account1), self.account1.username)
