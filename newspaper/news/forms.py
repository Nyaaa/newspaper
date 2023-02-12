from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category, Comment


class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all().order_by('name'), widget=forms.SelectMultiple)

    class Meta:
        model = Post
        fields = ['category', 'title', 'text']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("title") == cleaned_data.get("text"):
            raise ValidationError({
                "text": "Text and title cannot be identical"
            })
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
                'text': forms.Textarea(attrs={'placeholder': 'Post a new comment', 'rows': 5, 'class': 'form-control'}),
        }
