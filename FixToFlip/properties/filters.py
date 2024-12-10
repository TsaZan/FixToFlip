import django_filters

from FixToFlip.properties.models import Property, PropertyExpense


class PropertiesFilter(django_filters.FilterSet):
    sort = django_filters.ChoiceFilter(
        choices=[
            ("0", "Newest"),
            ("1", "Oldest"),
            ("2", "Lowest Credited Amount"),
            ("3", "Highest Credited Amount"),
        ],
        method="filter_by_sort",
        label="Sort By",
    )

    def filter_by_sort(self, queryset, name, value):
        if value == "0":
            return queryset.order_by("-bought_date")
        elif value == "1":
            return queryset.order_by("bought_date")
        elif value == "2":
            return queryset.order_by("-property_financial_information")
        elif value == "3":
            return queryset.order_by("property_financial_information")

        return queryset

    class Meta:
        model = Property
        fields = ["sort"]


class ExpensesFilter(django_filters.FilterSet):
    sort = django_filters.ChoiceFilter(
        choices=[
            ("0", "Lowest Expected Expense"),
            ("1", "Highest Expected Expense"),
        ],
        method="filter_by_sort",
        label="Sort By",
    )

    def filter_by_sort(self, queryset, name, value):

        if value == "0":
            return queryset.order_by("expected_expenses")
        elif value == "1":
            return queryset.order_by("-expected_expenses")

        return queryset

    class Meta:
        model = PropertyExpense
        fields = ["sort"]
