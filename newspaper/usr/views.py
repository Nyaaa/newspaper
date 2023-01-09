from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import NameChangeForm
from django.contrib.auth.models import Group, User
from django.urls import reverse_lazy
from news.models import Author
from django.contrib import messages


# Create your views here.
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class NameEditView(LoginRequiredMixin, UpdateView):
    template_name = 'account/name_edit.html'
    form_class = NameChangeForm
    model = User
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def upgrade_me(request):
    user = request.user
    authors = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors.user_set.add(user)
    if not Author.objects.filter(user=user).first():
        Author.objects.create(user=user)
        messages.success(request, 'Congratulations! You can now publish news and articles!')
    return redirect(reverse_lazy('profile'))
