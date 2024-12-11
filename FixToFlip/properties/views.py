from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView
from djmoney.money import Money
from rest_framework import generics, status
from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.dateparse import parse_date
from FixToFlip.choices import ExpenseTypeChoices, PropertyConditionChoices
from FixToFlip.credits.models import Credit
from FixToFlip.money_operations import sum_current_expenses
from FixToFlip.properties.filters import PropertiesFilter, ExpensesFilter
from FixToFlip.properties.forms import (
    PropertyAddForm,
    PropertyEditForm,
    PropertyDeleteForm,
    AddExpenseForm,
    AddCreditToPropertyForm,
    PropertyFinanceInformationForm,
    PropertyExpenseForm,
    ExpenseNotesForm,
)
from FixToFlip.properties.models import (
    Property,
    PropertyExpense,
    PropertyFinancialInformation,
    PropertyExpenseNotes,
)
from FixToFlip.properties.serializers import (
    PropertySerializer,
    PropertyExpenseSerializer,
    ExpenseNotesCreateSerializer,
)


class DashboardPropertiesView(LoginRequiredMixin, TemplateView):
    template_name = "properties/properties-list.html"
    filterset_class = PropertiesFilter
    login_url = "index"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        properties = Property.objects.filter(owner=self.request.user)
        sorted_properties = PropertiesFilter(self.request.GET, queryset=properties)
        properties = sorted_properties.qs.distinct()
        paginator = Paginator(properties, 5)
        page_number = self.request.GET.get("page")
        properties = paginator.get_page(page_number)

        if "q" in self.request.GET:
            q = self.request.GET.get("q", "")
            properties = Property.objects.filter(property_name__icontains=q)

        for property in properties:
            property.current_expenses = sum_current_expenses(property.id)

        context["search_placeholder"] = "Search property by title..."
        context["properties"] = properties
        context["filter"] = sorted_properties
        context["header_title"] = "Properties Dashboard"

        return context


@login_required(login_url="index")
def property_add_view(request):
    if request.method == "POST":
        property_form = PropertyAddForm(request.POST)
        property_financial_information_form = PropertyFinanceInformationForm(
            request.POST
        )
        expense_form = PropertyExpenseForm(request.POST)

        if (
            property_form.is_valid()
            and property_financial_information_form.is_valid()
            and expense_form.is_valid()
        ):
            property_form.instance.owner = request.user
            property = property_form.save()
            expense = expense_form.save(commit=False)
            expense.property = property
            expense.save()
            financial_information = property_financial_information_form.save(
                commit=False
            )
            financial_information.property = property
            financial_information.save()

            return redirect("dashboard_properties")

    else:
        property_form = PropertyAddForm()
        property_financial_information_form = PropertyFinanceInformationForm()
        expense_form = PropertyExpenseForm()

    context = {
        "property_form": property_form,
        "property_financial_information_form": property_financial_information_form,
        "expense_form": expense_form,
        "header_title": "Add Property",
    }

    return render(request, "properties/add-property.html", context)


class PropertyEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "properties/edit-property.html"
    model = Property
    fields = "__all__"

    property_form_class = PropertyEditForm()
    property_financial_information_form_class = PropertyFinanceInformationForm()
    expense_form_class = PropertyExpenseForm()
    success_url = reverse_lazy("dashboard_properties")
    login_url = "index"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["property_form"] = PropertyEditForm(instance=self.object)
        context["property_financial_information_form"] = PropertyFinanceInformationForm(
            instance=(
                self.object.property_financial_information.first()
                if self.object.property_financial_information.exists()
                else None
            )
        )
        context["expense_form"] = PropertyExpenseForm(
            instance=(
                self.object.property_expenses.first()
                if self.object.property_expenses.exists()
                else None
            )
        )
        context["header_title"] = "Edit Property"
        return context

    def test_func(self):
        property = self.get_object()
        return self.request.user == property.owner

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        property_form = PropertyEditForm(request.POST, instance=self.object)
        property_financial_information_form = PropertyFinanceInformationForm(
            request.POST,
            instance=(
                self.object.property_financial_information.first()
                if self.object.property_financial_information.exists()
                else None
            ),
        )
        expense_form = PropertyExpenseForm(
            request.POST,
            instance=(
                self.object.property_expenses.first()
                if self.object.property_expenses.exists()
                else None
            ),
        )

        if (
            property_form.is_valid()
            and property_financial_information_form.is_valid()
            and expense_form.is_valid()
        ):
            property_form.instance.owner = request.user
            property_form.save()

            expense = expense_form.save(commit=False)
            expense.property = self.object
            expense.save()

            financial_information = property_financial_information_form.save(
                commit=False
            )
            financial_information.property = self.object
            financial_information.save()

            return redirect("dashboard_properties")

        context = self.get_context_data()
        context["property_form"] = property_form
        context["property_financial_information_form"] = (
            property_financial_information_form
        )
        context["expense_form"] = expense_form

        return self.render_to_response(context)


class PropertyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Property
    success_url = reverse_lazy("dashboard_properties")
    login_url = "index"
    form_class = PropertyDeleteForm
    property_financial_information_form_class = PropertyFinanceInformationForm
    expense_form_class = PropertyExpenseForm
    template_name = "properties/delete-property.html"

    def test_func(self):
        property = self.get_object()
        return self.request.user == property.owner


class PropertyDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = "index"
    model = Property
    template_name = "properties/property-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["credit_form"] = AddCreditToPropertyForm(user=self.request.user)
        context["expenses"] = PropertyExpense.objects.filter(property=self.object)
        context["property_financial_information"] = (
            PropertyFinancialInformation.objects.filter(property=self.object)
        )
        context["credits"] = Credit.objects.filter(
            credit_owner_id=self.request.user.id,
            credit_financial_information__property_id=self.object.id,
        )
        context["today"] = date.today()
        context["head_title"] = "Property Details"
        return context

    def test_func(self):
        property = self.get_object()
        return self.request.user == property.owner

    def post(self, request, *args, **kwargs):
        property = self.get_object()
        form = AddCreditToPropertyForm(request.POST, user=self.request.user)

        if "remove_credit" in request.POST:
            credit_id = request.POST.get("remove_credit")
            finance_info = PropertyFinancialInformation.objects.filter(
                property=property, credit_id=credit_id
            )
            finance_info.update(credit=None, is_credited=False, credited_amount=0)

            messages.success(
                request, "The credit was successfully removed from the property."
            )
            return redirect("property_details", pk=property.id)

        if form.is_valid():
            finance_information = PropertyFinancialInformation.objects.filter(
                pk=property.pk
            )
            owned_credits = Credit.objects.filter(credit_owner_id=self.request.user.id)
            for credit in owned_credits:
                if credit.id == int(form.cleaned_data["credit"]):
                    if (
                        credit.remaining_credit_amount().amount
                        < form.cleaned_data["credited_amount"].amount
                    ):
                        errors = f"You cannot credit more than the credit remaining amount. \n Remaining amount: {credit.remaining_credit_amount()}"
                        return render(
                            request,
                            "properties/property-details.html",
                            {
                                "credit_form": form,
                                "property": property,
                                "errors": errors,
                            },
                        )

            finance_information.update(
                property=property,
                is_credited=True,
                credited_amount=form.cleaned_data["credited_amount"],
                credit=form.cleaned_data["credit"],
            )
            return redirect("property_details", pk=property.id)

        context = self.get_context_data()
        context["credit_form"] = form
        return self.render_to_response(context)


class DashboardExpensesView(LoginRequiredMixin, TemplateView):
    model = PropertyExpense
    template_name = "properties/expenses-list.html"
    login_url = "index"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        properties = Property.objects.filter(owner=self.request.user)
        expenses_list = PropertyExpense.objects.filter(property__in=properties)
        sorted_expenses = ExpensesFilter(self.request.GET, queryset=expenses_list)
        expenses_list = sorted_expenses.qs.distinct()
        paginator = Paginator(expenses_list, 5)
        page_number = self.request.GET.get("page")
        expenses = paginator.get_page(page_number)

        if "q" in self.request.GET:
            q = self.request.GET.get("q", "")
            expenses = PropertyExpense.objects.filter(
                property__property_name__icontains=q, property__in=properties
            )

        context["header_title"] = "Expenses Dashboard"
        context["search_placeholder"] = "Search expenses by property..."
        context["filter"] = sorted_expenses
        context["expenses"] = expenses

        return context


@login_required(login_url="index")
def add_expense(request, pk):
    expenses = get_object_or_404(PropertyExpense, pk=pk, property__owner=request.user)
    expenses_notes = PropertyExpenseNotes.objects.all().filter(
        relates_expenses=expenses
    )
    property = get_object_or_404(Property, id=expenses.property_id, owner=request.user)

    if request.method == "POST":
        notes_form = ExpenseNotesForm(request.POST)
        form = AddExpenseForm(request.POST)
        if form.is_valid() and notes_form.is_valid():
            notes_instance = notes_form.save(commit=False)
            field = form.cleaned_data["expense_types"]
            amount = form.cleaned_data["amount"]
            description = ExpenseTypeChoices(field).label
            notes_instance.expense_type = description
            notes_instance.expense_amount = amount
            notes_instance.relates_expenses = expenses
            notes_instance.save()

            current_value = getattr(expenses, field)
            setattr(expenses, field, current_value + amount)

            notes_form.save()
            expenses.save()
            return redirect("add_expense", pk=pk)
    else:
        form = AddExpenseForm()
        notes_form = ExpenseNotesForm()

    context = {
        "header_title": "Expenses Details",
        "form": form,
        "notes_form": notes_form,
        "expenses_notes": expenses_notes,
        "expenses": expenses,
        "property": property,
    }

    return render(request, "properties/expenses-details.html", context)


@login_required(login_url="index")
def delete_expense(request, pk):
    note = get_object_or_404(PropertyExpenseNotes, pk=pk)
    related_expense = note.relates_expenses
    expense_type = note.expense_type.lower().replace(" ", "_")

    if related_expense.property.owner != request.user:
        raise Http404("You do not have permission to delete this expense.")

    try:
        field = ExpenseTypeChoices.get_choice(note.expense_type)
    except ValueError as e:
        raise Http404(f"There is no field: {e}")

    if not hasattr(related_expense, field):
        raise Http404(f"There is no field: {field}")

    current_value = getattr(related_expense, field)

    amount = note.expense_amount

    new_value = current_value - amount
    new_value = max(new_value, Money(0, current_value.currency))
    setattr(related_expense, field, new_value)

    related_expense.save()
    note.delete()

    return redirect("add_expense", pk=related_expense.pk)


""" API Views """


class PropertyConditionChartData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        conditions = [choice[0] for choice in PropertyConditionChoices.choices]
        if not user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=403)

        data = {
            condition: Property.objects.filter(
                owner=user, property_condition=condition
            ).count()
            for condition in conditions
        }
        return Response(data)


class PropertyExpenseData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=403)

        start_date = request.GET.get("start_date", "")
        end_date = request.GET.get("end_date", "")

        start_date = parse_date(start_date) if start_date else None
        end_date = parse_date(end_date) if end_date else None

        notes_queryset = PropertyExpenseNotes.objects.filter(
            relates_expenses__property__owner=user
        )

        if start_date:
            notes_queryset = notes_queryset.filter(expense_date__gte=start_date)
        if end_date:
            notes_queryset = notes_queryset.filter(expense_date__lte=end_date)

        aggregated_expenses = notes_queryset.values("expense_type").annotate(
            total_amount=Sum("expense_amount")
        )

        expenses_data = {
            entry["expense_type"]: entry["total_amount"]
            for entry in aggregated_expenses
        }

        return Response(expenses_data)


class PropertyListApiView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)


class BulkPropertyCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PropertySerializer(
            data=request.data, many=True, context={"request": request}
        )

        if serializer.is_valid():
            created_properties = serializer.save()
            response_data = PropertySerializer(created_properties, many=True).data
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyApiView(generics.ListAPIView):
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Property.objects.filter(pk=pk, owner=self.request.user)

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = PropertySerializer


class PropertyExpensesApiView(generics.ListAPIView):
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return PropertyExpense.objects.filter(
            property_id=pk, property__owner=self.request.user
        )

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = PropertyExpenseSerializer


class PropertyExpenseNoteCreateAPIView(APIView):
    def post(self, request, pk, *args, **kwargs):
        try:
            related_expense = PropertyExpense.objects.get(id=pk)
        except PropertyExpense.DoesNotExist:
            return Response(
                {"error": "PropertyExpense not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ExpenseNotesCreateSerializer(
            data=request.data, context={"relates_expenses": related_expense}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
