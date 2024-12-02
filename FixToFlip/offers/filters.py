import django_filters
from FixToFlip.offers.models import Offer


class OffersFilter(django_filters.FilterSet):
    sort = django_filters.ChoiceFilter(
        choices=[
            ('0', 'Newest Offers'),
            ('1', 'Oldest Offers'),
            ('2', 'Lowest Price'),
            ('3', 'Highest Price'),
        ],
        method='filter_by_sort',
    )

    def filter_by_sort(self, queryset, name, value):
        if value == '0':
            return queryset.order_by('-created_at')
        elif value == '1':
            return queryset.order_by('created_at')
        elif value == '2':
            return queryset.order_by('listed_price')
        elif value == '3':
            return queryset.order_by('-listed_price')

        return queryset

    class Meta:
        model = Offer
        fields = ['sort']
