from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category

class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all().order_by('name'), widget=forms.SelectMultiple)

    class Meta:
        model = Post
        fields = ['category', 'author', 'title', 'text']

