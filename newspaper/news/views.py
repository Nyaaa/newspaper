from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime

# Create your views here.
class PostList(ListView):
    model = Post
    ordering = '-created'
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
