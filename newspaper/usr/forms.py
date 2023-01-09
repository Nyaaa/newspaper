from django import forms
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SSignupForm
from django.contrib.auth.models import Group, User
from news.templatetags.custom_filters import CENSOR_LIST


class BasicSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
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
