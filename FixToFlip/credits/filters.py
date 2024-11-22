import django_filters
from FixToFlip.credits.models import Credit


class CreditsFilter(django_filters.FilterSet):
    sort = django_filters.ChoiceFilter(
        choices=[
            ('0', 'Newest Credits'),
            ('1', 'Oldest Credits'),
            ('2', 'Lowest Monthly Payment'),
            ('3', 'Highest Monthly Payment'),
            ('4', 'Lowest Interest Rate'),
            ('5', 'Highest Interest Rate'),
        ],
        method='filter_by_sort',
        label='Sort By'
    )

    def filter_by_sort(self, queryset, name, value):
        if value == '0':
            return queryset.order_by('-credit_start_date')
        elif value == '1':
            return queryset.order_by('credit_start_date')
        elif value == '2':
            return queryset.order_by('monthly_payment')
        elif value == '3':
            return queryset.order_by('-monthly_payment')
        elif value == '4':
            return queryset.order_by('credit_interest')
        elif value == '5':
            return queryset.order_by('-credit_interest')
        return queryset

    class Meta:
        model = Credit
        fields = ['sort']