from django.contrib import messages
from django.shortcuts import render, redirect

from FixToFlip.credits.forms import CreditAddForm
from FixToFlip.credits.models import Credit


def CreditsView(request):
    pass


def CreditDetailsView(request, pk):
    pass


def AddCreditView(request):
    if request.method == 'POST':
        form = CreditAddForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Credit added successfully!')
            form = CreditAddForm()
    else:
        form = CreditAddForm()  # If not POST, create an empty form

    context = {
        "credits": Credit.objects.all(),
        "CreditForm": form  # Pass the form instance to the template
    }
    return render(request, 'credits/add-credit.html', context)


def EditCreditView(request, pk):
    pass


def DeleteCreditView(request, pk):
    pass


def CreditPaymentView(request, pk):
    pass
