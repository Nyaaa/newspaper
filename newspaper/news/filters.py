import django_filters
from django import forms
from .models import Post, Author


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    created = django_filters.DateFilter(field_name='created', lookup_expr='gt', widget=forms.DateInput(attrs={'type': 'date'}))  # TODO change to range
    author = django_filters.ModelChoiceFilter(field_name='author', empty_label='All authors', lookup_expr='exact', queryset=Author.objects.all())

    class Meta:
        model = Post
        fields = ['title', 'author', 'created']
