from django.shortcuts import render

from FixToFlip.offers.models import Offer


def offers_main_page(request):
    context = {'offers': Offer.objects.all()}
    return render(request, 'offers/offers_main_page.html', context)


def details_offer(request, pk):
    pass


def add_offer(request):
    pass


def edit_offer(request, pk):
    pass


def delete_offer(request, pk):
    pass
