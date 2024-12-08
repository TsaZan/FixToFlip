from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView, DeleteView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from FixToFlip.offers.filters import OffersFilter
from FixToFlip.offers.forms import OfferBaseForm, OfferAddForm, PropertyOfferEditForm, OfferEditForm
from FixToFlip.offers.models import Offer
from FixToFlip.offers.serializers import OfferAPISerializer
from FixToFlip.properties.forms import PropertyAddForm
from FixToFlip.properties.models import Property


class DashboardOffersView(LoginRequiredMixin, TemplateView):
    template_name = 'offers/offers-list.html'
    filterset_class = OffersFilter
    login_url = 'index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offers_list = Offer.objects.filter(listed_property__owner=self.request.user)
        offers_filter = OffersFilter(self.request.GET, queryset=offers_list)
        sorted_offers = offers_filter.qs.distinct()
        paginator = Paginator(sorted_offers, 5)
        page_number = self.request.GET.get('page')
        offers = paginator.get_page(page_number)

        if 'q' in self.request.GET:
            q = self.request.GET.get('q', '')
            offers = Offer.objects.filter(listed_property__property_name__icontains=q)

        context['offers'] = offers
        context['filter'] = offers_filter
        context['search_placeholder'] = 'Search offer by property name...'
        context['header_title'] = 'Offers Dashboard'

        return context


@login_required(login_url='index')
def add_offer_view(request, pk):
    if request.method == 'POST' and not Offer.objects.filter(listed_property__pk=pk).exists():
        form = OfferAddForm(request.POST)

        if form.is_valid() and request.user == Property.objects.get(pk=pk).owner:
            offer = form.save(commit=False)
            offer.listed_property = Property.objects.get(pk=pk)
            offer.save()
            pk = offer.pk
            return redirect('edit_offer', pk=pk)
    elif Offer.objects.filter(listed_property__pk=pk).exists():
        pk = Offer.objects.get(listed_property__pk=pk).pk
        return redirect('edit_offer', pk=pk)
    else:
        form = OfferAddForm()
    return render(request, 'offers/add-offer.html', {'form': form})


class EditOfferView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Offer
    fields = '__all__'
    template_name = 'offers/edit-offer.html'
    success_url = reverse_lazy('offers_main_page')

    def test_func(self):
        offer = self.get_object()
        return self.request.user == offer.listed_property.owner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['offer_form'] = OfferBaseForm(instance=self.object)
        context['property_form'] = PropertyAddForm(instance=self.object.listed_property)
        context['header_title'] = 'Edit Offer'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        offer_form = OfferEditForm(request.POST, request.FILES, instance=self.object)
        property_form = PropertyOfferEditForm(request.POST, instance=self.object.listed_property)
        property_form.property_name = self.object.listed_property.property_name
        user_profile = property_form.instance.owner.profile

        if user_profile.profile_type == 'Personal':
            if user_profile.user.first_name and user_profile.user.last_name and user_profile.phone_number:
                pass
            else:
                property_form.add_error(None, 'As a personal profile, please provide your first name, last name, '
                                              'and phone number before publishing a listing.')
        elif user_profile.profile_type == 'Company':
            if user_profile.company_name and user_profile.company_phone:
                pass
            else:
                property_form.add_error(None, 'As a company profile, you must provide a company name and a phone '
                                              'number before publishing a listing')
        elif not user_profile.profile_type:
            property_form.add_error(None, f'Please set up your profile type and provide the necessary details before '
                                          'publishing a listing.')

        if offer_form.is_valid() and property_form.is_valid():
            offer_form.save()
            property_form.save()
            return redirect('offers_main_page')

        context = self.get_context_data()
        context['offer_form'] = offer_form
        context['property_form'] = property_form
        return self.render_to_response(context)


class OfferDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Offer
    fields = '__all__'
    template_name = 'offers/delete-offer.html'
    success_url = reverse_lazy('offers_main_page')

    def test_func(self):
        offer = self.get_object()
        return self.request.user == offer.listed_property.owner


'''API Views'''


class AllOffersAPIView(APIView):
    serializer_class = OfferAPISerializer
    permission_classes = [AllowAny]

    def get(self, request):
        offers = Offer.objects.filter(is_published=True)
        serializer = OfferAPISerializer(offers, many=True)
        return Response(serializer.data)


class OfferAPIView(APIView):
    serializer_class = OfferAPISerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        serializer = OfferAPISerializer(offer)
        return Response(serializer.data)
