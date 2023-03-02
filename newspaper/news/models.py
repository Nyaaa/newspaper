from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Sum


# Create your models here.
class LikeManager(models.Manager):
    use_for_related_fields = True

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class Like(models.Model):
    class Votes(models.IntegerChoices):
        LIKE = 1
        DISLIKE = -1

    vote = models.SmallIntegerField(choices=Votes.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    objects = LikeManager()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _rating = models.IntegerField(default=0, db_column='rating')

    @property
    def rating(self):
        return self._rating

    def update_rating(self):
        self._rating = 0

        # posts by Author
        self._rating += 3 * Post.objects.filter(author=self).aggregate(
            Sum('votes__vote')).get('votes__vote__sum') or 0
        # comments to posts by Author
        self._rating += Comment.objects.filter(post__author=self).aggregate(
            Sum('votes__vote')).get('votes__vote__sum') or 0
        # comments by Author
        self._rating += Comment.objects.filter(user=self.user).aggregate(
            Sum('votes__vote')).get('votes__vote__sum') or 0

        self.save()

    def __str__(self):
        return f'{self.user.get_full_name() or self.user}'

    def short_name(self):
        return f'{self.user.first_name[0]}. {self.user.last_name}'


class CategoryUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through=CategoryUser)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = "categories"


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
    votes = GenericRelation(Like, related_query_name='posts')

    def __str__(self):
        return f'{self.title.title()}'

    def get_absolute_url(self):
        if self.type == Post.PostType.ARTICLE:
            cat = '/articles/'
        else:
            cat = '/news/'
        return f'{cat}{self.pk}'
        # return reverse('post_detail', args=[str(self.id)])

    def get_full_absolute_url(self):
        domain = Site.objects.get_current().domain
        return f'{domain}{self.get_absolute_url()}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    votes = GenericRelation(Like, related_query_name='comments')

    def __str__(self):
        return f'[{self.post}] - {self.text}'
