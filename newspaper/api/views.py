from .serializers import PostSerializer
from rest_framework import viewsets
from news.models import Post, Author
from .permissions import UserPermission


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = (UserPermission,)
    serializer_class = PostSerializer
    queryset = Post.objects.filter(type=Post.PostType.NEWS)
    filterset_fields = ['created', 'category']

    def perform_create(self, serializer):
        user = Author.objects.get(user=self.request.user)
        path = self.request.META.get('PATH_INFO')
        if 'articles' in path:
            post_type = Post.PostType.ARTICLE
        serializer.save(author=user, type=post_type)


class ArticleViewSet(NewsViewSet):
    queryset = Post.objects.filter(type=Post.PostType.ARTICLE)
