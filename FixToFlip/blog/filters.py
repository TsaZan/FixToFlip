import django_filters
from .models import BlogPost


class BlogPostsFilter(django_filters.FilterSet):
    sort = django_filters.ChoiceFilter(
        choices=[
            ("0", "Newest"),
            ("1", "Oldest"),
            ("2", "Most Comments"),
            ("3", "Least Comments"),
        ],
        method="filter_by_sort",
        label="Sort By",
    )

    def filter_by_sort(self, queryset, name, value):
        if value == "0":
            return queryset.order_by("-created_at")
        elif value == "1":
            return queryset.order_by("created_at")
        elif value == "2":
            return queryset.order_by("-comments_count")
        elif value == "3":
            return queryset.order_by("comments_count")
        return queryset

    class Meta:
        model = BlogPost
        fields = ["sort"]
