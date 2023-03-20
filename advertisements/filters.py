import django_filters

from advertisements.models import Advertisement


# ----------------------------------------------------------------------------------------------------------------------
# Custom filters
class TitleFilter(django_filters.rest_framework.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Advertisement
        fields = ('title',)
