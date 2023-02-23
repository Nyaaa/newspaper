from django import forms
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SSignupForm
from django.contrib.auth.models import Group, User
from news.templatetags.custom_filters import CENSOR_LIST
from news.models import Category


class BasicSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')
    sub_check = forms.BooleanField(initial=True, required=False, label='Subscribe to our weekly digest')

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data['sub_check']:
            for i in Category.objects.all():
                i.subscribers.add(user)
        return user


class SocialSignupForm(SSignupForm):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')

    def save(self, request):
        user = super(SocialSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        return user


class NameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        for name in NameChangeForm.Meta.fields:
            dirty = cleaned_data.get(name)
            if dirty in CENSOR_LIST:
                self._errors[name] = self.error_class(['Name is not allowed'])
            elif len(dirty) > 15:
                self._errors[name] = self.error_class(['Name is too long'])

        return cleaned_data


class SubscribeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                             widget=forms.CheckboxSelectMultiple,
                                                             )
        self.fields['name'].initial = Category.objects.filter(subscribers=self.user).values_list('id', flat=True)

    class Meta:
        model = Category
        fields = ['name']

    def clean(self):
        user = self.user
        cleaned_data = super().clean()
        categories = Category.objects.all()
        to_sub = cleaned_data['name']

        for cat in categories:
            subs = cat.subscribers.all()
            if cat in to_sub and user not in subs:
                cat.subscribers.add(user)
            elif cat not in to_sub and user in subs:
                cat.subscribers.remove(user)

        return cleaned_data
