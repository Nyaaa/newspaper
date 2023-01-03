import django_filters
from django import forms
from .models import Post


class DateInput(forms.DateInput):
    input_type = 'date'


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    created = django_filters.DateFilter(field_name='created', lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        widgets = {'created': DateInput(),}
        fields = ['title', 'author', 'created']