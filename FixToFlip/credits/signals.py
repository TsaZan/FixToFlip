from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from djmoney.money import Money

from FixToFlip.credits.models import CreditPayment
from FixToFlip.properties.models import PropertyFinancialInformation, PropertyExpenseNotes, PropertyExpense


@receiver(post_save, sender=CreditPayment)
def create_expense_notes(sender, instance, created, **kwargs):
    if created:
        credited_properties = (PropertyFinancialInformation.objects
                               .filter(credit_id=instance.credit_id, credited_amount__gt=0))
        total_credit_amount = credited_properties.aggregate(Sum('credited_amount'))

        for property in credited_properties:
            credit_share = property.credited_amount.amount / total_credit_amount['credited_amount__sum']
            credit_interest_expense = instance.interest_amount * credit_share
            PropertyExpenseNotes.objects.create(
                notes=f'Credit Payment for {instance.credit.bank_name} credit (Payment ID: {instance.id}).',
                expense_type='Credit Interest',
                expense_amount=credit_interest_expense,
                expense_date=instance.payment_date,
                relates_expenses=property.property.property_expenses.first()
            )

            PropertyExpense.objects.filter(id=property.property.property_expenses.first().id) \
                .update(credit_interest=property.property.property_expenses.first().credit_interest.amount
                                        + credit_interest_expense.amount)


@receiver(post_delete, sender=CreditPayment)
def delete_related_expense_notes(sender, instance, **kwargs):
    credited_properties = (PropertyFinancialInformation.objects
                           .filter(credit_id=instance.credit_id, credited_amount__gt=0))
    total_credit_amount = credited_properties.aggregate(Sum('credited_amount'))

    if total_credit_amount['credited_amount__sum'] == 0:
        return

    expense_notes = PropertyExpenseNotes.objects.filter(
        notes__icontains=f'Payment ID: {instance.id}'
    )

    for property in credited_properties:
        credit_share = property.credited_amount.amount / total_credit_amount['credited_amount__sum']
        credit_interest_expense = instance.interest_amount * credit_share

        related_expense = property.property.property_expenses.first()
        if related_expense:
            related_expense.credit_interest -= credit_interest_expense
            if related_expense.credit_interest < Money(0, related_expense.credit_interest.currency):
                related_expense.credit_interest = Money(0, related_expense.credit_interest.currency)
            related_expense.save()

    expense_notes.delete()
