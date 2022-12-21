from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _rating = models.IntegerField(default=0, db_column='rating')

    @property
    def rating(self):
        return self._rating

    def update_rating(self):
        self._rating = 0

        # posts by Author
        self._rating += Post.objects.filter(author=self).aggregate(models.Sum('rating'))['rating__sum'] * 3
        # comments to posts by Author
        self._rating += Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum']
        # comments by Author
        self._rating += Comment.objects.filter(user=self.user).aggregate(models.Sum('rating'))['rating__sum']

        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    class PostType(models.IntegerChoices):
        ARTICLE = 1
        NEWS = 2

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.PositiveSmallIntegerField(choices=PostType.choices, default=PostType.NEWS)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through=PostCategory)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
