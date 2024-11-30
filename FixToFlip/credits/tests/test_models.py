from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from djmoney.money import Money
from FixToFlip.credits.models import Credit, CreditPayment
from django.contrib.auth import get_user_model
from datetime import date, timedelta

User = get_user_model()


class CreditModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.credit = Credit.objects.create(
            bank_name="Test Bank",
            credit_amount=Money(10000, 'EUR'),
            credit_interest=3.5,
            monthly_payment=Money(500, 'EUR'),
            credit_start_date=date.today() - timedelta(days=365),
            credit_term=date.today() + timedelta(days=730),
            credit_type="Mortgage",
            credit_owner=self.user,
        )

    def test_credit_str(self):
        self.assertEqual(
            str(self.credit),
            f'{self.credit.bank_name} - {self.credit.credit_start_date} - {self.credit.credit_amount}'
        )

    def test_remaining_credit_amount(self):
        self.assertEqual(self.credit.remaining_credit_amount(), self.credit.credit_amount)


class CreditPaymentModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.credit = Credit.objects.create(
            bank_name="Test Bank",
            credit_amount=Money(10000, 'EUR'),
            credit_interest=3.5,
            monthly_payment=Money(500, 'EUR'),
            credit_start_date=date.today() - timedelta(days=365),
            credit_term=date.today() + timedelta(days=730),
            credit_type="Mortgage",
            credit_owner=self.user,
        )
        self.payment = CreditPayment.objects.create(
            payment_date=date.today(),
            principal_amount=Money(2000, 'EUR'),
            interest_amount=Money(100, 'EUR'),
            credit=self.credit,
        )

    def test_full_payment(self):
        self.assertEqual(
            self.payment.full_payment(),
            Money(2100, 'EUR')
        )

    def test_payment_str(self):
        self.assertEqual(
            str(self.payment),
            f"{self.payment.payment_date} - {self.payment.full_payment()} - {self.credit.bank_name}"
        )


