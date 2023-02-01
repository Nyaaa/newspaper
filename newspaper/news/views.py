from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Author, Comment
from .filters import PostFilter
from .forms import PostForm
from django.utils import timezone
from .tasks import notification


# Create your views here.
class PostList(ListView):
    model = Post
    ordering = '-created'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        path = self.request.META.get('PATH_INFO')
        if path == '/articles/':
            queryset = queryset.filter(type=Post.PostType.ARTICLE)
        else:
            queryset = queryset.filter(type=Post.PostType.NEWS)

        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        path = self.request.META.get('PATH_INFO')
        if path == '/articles/':
            context['page_title'] = 'articles'
        elif path == '/news/':
            context['page_title'] = 'news'
        else:
            context['page_title'] = 'search results'
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.get_object())
        return context


class PostCreate(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)
    success_message = 'Post "%(title)s" was created successfully'

    def form_valid(self, form):
        post = form.save(commit=False)
        path = self.request.META.get('PATH_INFO')
        post.author = Author.objects.get(user=self.request.user)
        if path == '/articles/create/':
            post.type = Post.PostType.ARTICLE
        response = super().form_valid(form)
        notification.delay(pk=form.instance.pk)  # Celery task, see tasks.py
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now()
        author = Author.objects.get(user=self.request.user)
        post_num = Post.objects.filter(author=author,
                                       created__range=[today - timezone.timedelta(days=1), today]
                                       ).count()
        if post_num >= 3:
            context['can_post'] = False
        else:
            context['can_post'] = True
        return context


class PostUpdate(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)
    success_message = 'Post "%(title)s" was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_post'] = True
        return context


class PostDelete(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post',)
    success_message = "Post was deleted successfully"


class SearchResults(ListView):
    model = Post
    template_name = 'posts.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        ).order_by('-created')
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'search results'
        return context


class HomeView(TemplateView):
    template_name = 'flatpages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_posts'] = Post.objects.all().order_by('-rating')[0:3]
        return context
