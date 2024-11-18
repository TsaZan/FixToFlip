from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView
from rest_framework import generics
from django.shortcuts import render
from django.core.paginator import Paginator

from FixToFlip.choices import ExpenseTypeChoices
from FixToFlip.credits.models import Credit
from FixToFlip.money_operations import sum_current_expenses
from FixToFlip.properties.forms import PropertyAddForm, \
    PropertyEditForm, PropertyDeleteForm, AddExpenseForm, AddCreditToPropertyForm, PropertyFinanceInformationForm, \
    PropertyExpenseForm, ExpenseNotesForm
from FixToFlip.properties.models import Property, PropertyExpense, PropertyFinancialInformation, PropertyExpenseNotes
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
        context['header_title'] = 'Properties Dashboard'

        return context


@login_required
def property_add_view(request):
    if request.method == 'POST':
        property_form = PropertyAddForm(request.POST)
        property_financial_information_form = PropertyFinanceInformationForm(request.POST)
        expense_form = PropertyExpenseForm(request.POST)

        if property_form.is_valid() and property_financial_information_form.is_valid() and expense_form.is_valid():
            property_form.instance.owner = request.user
            property = property_form.save()
            expense = expense_form.save(commit=False)
            expense.property = property
            expense.save()
            financial_information = property_financial_information_form.save(commit=False)
            financial_information.property = property
            financial_information.save()

            return redirect('dashboard_properties')

    else:
        property_form = PropertyAddForm()
        property_financial_information_form = PropertyFinanceInformationForm()
        expense_form = PropertyExpenseForm()

    context = {
        'property_form': property_form,
        'property_financial_information_form': property_financial_information_form,
        'expense_form': expense_form
    }

    return render(request, 'dashboard/add-property.html', context)


class PropertyEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'dashboard/edit-property.html'
    model = Property
    fields = '__all__'

    property_form_class = PropertyEditForm()
    property_financial_information_form_class = PropertyFinanceInformationForm()
    expense_form_class = PropertyExpenseForm()
    success_url = reverse_lazy('dashboard_properties')
    login_url = 'index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_form'] = PropertyEditForm(instance=self.object)
        context['property_financial_information_form'] = PropertyFinanceInformationForm(
            instance=self.object.property_financial_information.first() if self.object.property_financial_information.exists() else None
        )
        context['expense_form'] = PropertyExpenseForm(
            instance=self.object.property_expenses.first() if self.object.property_expenses.exists() else None
        )
        return context

    def test_func(self):
        property = self.get_object()
        return self.request.user == property.owner

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        property_form = PropertyEditForm(request.POST, instance=self.object)
        property_financial_information_form = PropertyFinanceInformationForm(
            request.POST,
            instance=self.object.property_financial_information.first() if self.object.property_financial_information.exists() else None
        )
        expense_form = PropertyExpenseForm(
            request.POST,
            instance=self.object.property_expenses.first() if self.object.property_expenses.exists() else None
        )

        if property_form.is_valid() and property_financial_information_form.is_valid() and expense_form.is_valid():
            property_form.instance.owner = request.user
            property_form.save()

            # Save the expenses form
            expense = expense_form.save(commit=False)
            expense.property = self.object
            expense.save()

            # Save the financial information form
            financial_information = property_financial_information_form.save(commit=False)
            financial_information.property = self.object
            financial_information.save()

            return redirect('dashboard_properties')

        context = self.get_context_data()
        context['property_form'] = property_form
        context['property_financial_information_form'] = property_financial_information_form
        context['expense_form'] = expense_form
        return self.render_to_response(context)


class PropertyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Property
    success_url = reverse_lazy('dashboard_properties')
    login_url = 'index'
    form_class = PropertyDeleteForm
    property_financial_information_form_class = PropertyFinanceInformationForm
    expense_form_class = PropertyExpenseForm
    template_name = 'dashboard/delete-property.html'

    def test_func(self):
        property = self.get_object()
        return self.request.user == property.owner


class PropertyDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = 'index'
    model = Property
    template_name = 'dashboard/property-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['credit_form'] = AddCreditToPropertyForm(user=self.request.user)
        context['expenses'] = PropertyExpense.objects.filter(property=self.object)
        context['property_financial_information'] = PropertyFinancialInformation.objects.filter(property=self.object)
        context['credits'] = Credit.objects.filter(credit_owner_id=self.request.user.id,
                                                   credit_financial_information__property_id=self.object.id,
                                                   )
        context['today'] = date.today()
        context['head_title'] = 'Property Details'
        return context

    def post(self, request, *args, **kwargs):
        property = self.get_object()
        form = AddCreditToPropertyForm(request.POST, user=self.request.user)
        if form.is_valid():
            finance_information = PropertyFinancialInformation.objects.filter(pk=property.pk)
            finance_information.update(
                property=property,
                is_credited=True,
                credited_amount=form.cleaned_data['credited_amount'],
                credit=form.cleaned_data['credit']

            )
            return redirect('property_details', pk=property.id)

        context = self.get_context_data()
        context['credit_form'] = form
        return self.render_to_response(context)

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
        context['header_title'] = 'Expenses Dashboard'

        context['expenses'] = expenses

        return context


@login_required
def add_expense(request, pk):
    expenses = get_object_or_404(PropertyExpense, pk=pk)
    expenses_notes = PropertyExpenseNotes.objects.all().filter(relates_expenses=expenses)
    property = Property.objects.get(id=expenses.property_id)

    if request.method == 'POST':
        notes_form = ExpenseNotesForm(request.POST)
        form = AddExpenseForm(request.POST)
        if form.is_valid() and notes_form.is_valid():
            notes_instance = notes_form.save(commit=False)
            field = form.cleaned_data['expense_types']
            amount = form.cleaned_data['amount']
            description = ExpenseTypeChoices(field).label
            notes_instance.expense_type = description
            notes_instance.expense_amount = amount
            notes_instance.relates_expenses = expenses
            notes_instance.save()

            current_value = getattr(expenses, field)
            setattr(expenses, field, current_value + amount)

            notes_form.save()
            expenses.save()
            return redirect('add_expense', pk=pk)
    else:
        form = AddExpenseForm()
        notes_form = ExpenseNotesForm()

    context = {
        'header_title': 'Add Expenses',
        'form': form,
        'notes_form': notes_form,
        'expenses_notes': expenses_notes,
        'expenses': expenses,
        'property': property,
    }

    return render(request, 'dashboard/expenses-details.html', context)


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
