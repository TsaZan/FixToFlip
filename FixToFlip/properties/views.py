from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView

from rest_framework import generics
from django.shortcuts import render
from django.core.paginator import Paginator


from FixToFlip.money_operations import sum_current_expenses
from FixToFlip.properties.forms import PropertyAddForm, PropertyExpenseForm, PropertyFinancialInformationForm
from FixToFlip.properties.models import Property, PropertyExpense
from FixToFlip.properties.serializers import PropertySerializer, PropertyExpenseSerializer


class DashboardPropertiesView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/properties-list.html'
    login_url = 'index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        properties = Property.objects.filter(owner=self.request.user)
        paginator = Paginator(properties, 5)
        page_number = self.request.GET.get('page')
        properties = paginator.get_page(page_number)
        for property in properties:
            property.current_expenses = sum_current_expenses(property.id)
        context['properties'] = properties

        return context


def property_add_view(request):
    if request.method == 'POST':
        property_form = PropertyAddForm(request.POST)
        property_form.instance.country = property_form.country
        property_financial_information_form = PropertyFinancialInformationForm(request.POST)
        expense_form = PropertyExpenseForm(request.POST)

        if property_form.is_valid() and property_financial_information_form.is_valid() and expense_form.is_valid():
            property_form.instance.owner = request.user
            property = property_form.save()
            property_financial_information = property_financial_information_form.save(commit=False)
            expense = expense_form.save(commit=False)
            expense.property = property
            expense.save()
            if property_financial_information.credited_amount:
                property_financial_information.is_credited = True
                property_financial_information.property = property
                property_financial_information.save()

            return redirect('dashboard_properties')

    else:
        property_form = PropertyAddForm()
        property_financial_information_form = PropertyFinancialInformationForm()
        expense_form = PropertyExpenseForm()

    context = {
        'property_form': property_form,
        'property_financial_information_form': property_financial_information_form,
        'expense_form': expense_form
    }

    return render(request, 'dashboard/add-property.html', context)


class PropertyDetailsView(LoginRequiredMixin, DetailView):
    login_url = 'index'

    model = Property
    template_name = 'dashboard/property-details.html'


class DashboardExpensesView(LoginRequiredMixin, TemplateView):
    model = PropertyExpense
    template_name = 'dashboard/expenses-list.html'
    login_url = 'index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        properties = Property.objects.filter(owner=self.request.user)
        expenses_list = PropertyExpense.objects.filter(property__in=properties)
        paginator = Paginator(expenses_list, 5)
        page_number = self.request.GET.get('page')
        expenses = paginator.get_page(page_number)

        context['expenses'] = expenses

        return context


''' React Views '''


class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class PropertyDetailsView(generics.ListAPIView):
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Property.objects.filter(pk=pk)

    serializer_class = PropertySerializer


class PropertyExpensesView(generics.ListAPIView):
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return PropertyExpense.objects.filter(property_id=pk)

    serializer_class = PropertyExpenseSerializer
