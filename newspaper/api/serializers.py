from news.models import Post, Author
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    type = serializers.StringRelatedField(default=Post.PostType.NEWS, read_only=True)

    class Meta:
        model = Post
        exclude = ('title', 'text')
