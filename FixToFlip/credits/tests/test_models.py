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


class CreditViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
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

    def test_dashboard_credits(self):
        response = self.client.get(reverse('dashboard_credits'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.credit.bank_name)

    def test_credit_add_view(self):
        data = {
            "bank_name": "New Bank",
            "credit_amount_0": "5000",  # MoneyField split into amount and currency
            "credit_amount_1": "EUR",
            "credit_interest": 2.5,
            "monthly_payment_0": "200",
            "monthly_payment_1": "EUR",
            "credit_start_date": date.today(),
            "credit_term": date.today() + timedelta(days=365),
            "credit_type": "Mortgage",
        }
        response = self.client.post(reverse('add_credit'), data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Credit.objects.filter(bank_name="New Bank").exists())

    def test_credit_details(self):
        response = self.client.get(reverse('credit_details', args=[self.credit.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.credit.bank_name)

    def test_credit_edit(self):
        data = {
            "bank_name": "Edited Bank",
            "credit_amount_0": "8000",
            "credit_amount_1": "EUR",
            "credit_interest": 3.0,
            "monthly_payment_0": "300",
            "monthly_payment_1": "EUR",
            "credit_start_date": self.credit.credit_start_date,
            "credit_term": self.credit.credit_term,
            "credit_type": "Mortgage",
        }
        response = self.client.post(reverse('edit_credit', args=[self.credit.id]), data)
        self.assertEqual(response.status_code, 302)
        self.credit.refresh_from_db()
        self.assertEqual(self.credit.bank_name, "Edited Bank")
        self.assertEqual(self.credit.credit_amount, Money(8000, 'EUR'))

    def test_credit_delete(self):
        response = self.client.post(reverse('delete_credit', args=[self.credit.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Credit.objects.filter(id=self.credit.id).exists())
