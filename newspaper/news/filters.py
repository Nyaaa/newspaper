from django_filters import CharFilter, FilterSet, ModelChoiceFilter, DateFilter
from django import forms
from .models import Post, Author, Category
from django_filters.widgets import RangeWidget


class PostFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    created_from = DateFilter(field_name='created', lookup_expr='gt', widget=forms.DateInput(attrs={'type': 'date'}))
    created_to = DateFilter(field_name='created', lookup_expr='lt', widget=forms.DateInput(attrs={'type': 'date'}))
    author = ModelChoiceFilter(field_name='author', empty_label='All authors', lookup_expr='exact', queryset=Author.objects.all())
    category = ModelChoiceFilter(field_name='category', empty_label='All categories', queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['created_from', 'created_to', 'title', 'author', 'category']
