from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView
from rest_framework import generics
from django.shortcuts import render
from django.core.paginator import Paginator
from FixToFlip.money_operations import sum_current_expenses
from FixToFlip.properties.forms import PropertyAddForm, PropertyExpenseForm, PropertyFinancialInformationForm, \
    PropertyEditForm, PropertyDeleteForm
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


@login_required
def property_add_view(request):
    if request.method == 'POST':
        property_form = PropertyAddForm(request.POST)
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


class PropertyEditView(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/edit-property.html'
    property_form = PropertyEditForm
    fields = '__all__'
    property_financial_information_form_class = PropertyFinancialInformationForm
    expense_form_class = PropertyExpenseForm
    success_url = reverse_lazy('dashboard_properties')
    login_url = 'index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_form'] = PropertyEditForm(instance=self.object)
        context['property_financial_information_form'] = PropertyFinancialInformationForm(instance=self.object)
        context['expense_form'] = PropertyExpenseForm(instance=self.object)
        return context

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)


class PropertyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Property
    success_url = reverse_lazy('dashboard_properties')
    login_url = 'index'
    form_class = PropertyDeleteForm
    property_financial_information_form_class = PropertyFinancialInformationForm
    expense_form_class = PropertyExpenseForm
    template_name = 'dashboard/delete-property.html'

    def test_func(self):
        property = self.get_object()
        return self.request.user == property.owner


class PropertyDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = 'index'

    model = Property
    template_name = 'dashboard/property-details.html'

    def test_func(self):
        property = self.get_object()
        return self.request.user == property.owner


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


class PropertyListApiView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class PropertyApiView(generics.ListAPIView):
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Property.objects.filter(pk=pk)

    serializer_class = PropertySerializer


class PropertyExpensesApiView(generics.ListAPIView):
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return PropertyExpense.objects.filter(property_id=pk)

    serializer_class = PropertyExpenseSerializer
