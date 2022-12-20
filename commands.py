print('imports...')
from news.models import *
import random

print('creating users...')
u1 = User.objects.create_user('user01')
u2 = User.objects.create_user('user02')

a1 = Author.objects.create(user=u1)
a2 = Author.objects.create(user=u2)

print('creating data...')
c1 = Category.objects.create(name='Facepalm')
c2 = Category.objects.create(name='Awww')
c3 = Category.objects.create(name='LOL')
c4 = Category.objects.create(name='Nope')

p1 = Post.objects.create(author=a1, type='a', title='Test article #1', text="Lorem ipsum")
p2 = Post.objects.create(author=a2, type='a', title='Test article #2', text="Lorem ipsum")
p3 = Post.objects.create(author=a1, type='n', title='Test news piece #1', text="Lorem ipsum")

PostCategory.objects.create(post=p1, category=c1)
PostCategory.objects.create(post=p2, category=c2)
PostCategory.objects.create(post=p3, category=c3)
PostCategory.objects.create(post=p3, category=c4)

c1 = Comment.objects.create(post=p1, user=u1, text='comment01')
c2 = Comment.objects.create(post=p2, user=u1, text='comment02')
c3 = Comment.objects.create(post=p3, user=u2, text='comment03')
c4 = Comment.objects.create(post=p1, user=u1, text='comment04')
c5 = Comment.objects.create(post=p2, user=u2, text='comment05')

obj = [p1, p2, p3, c1, c2, c3, c4, c5]

for i in obj:
    c = bool(random.getrandbits(1))
    i.like() if c else i.dislike()

print('top ratings:')
a1.update_rating()
a2.update_rating()

print('top author:')
Author.objects.all().order_by('_rating').values('user__username', '_rating').last()

print('top article:')
Post.objects.filter(type='a').order_by('rating').values('created', 'author__user__username', 'rating', 'title').last()
p = Post.objects.filter(type='a').order_by('rating').last()
print('preview:')
p.preview()
print('comments:')
Comment.objects.filter(post=p).values('created', 'user', 'rating', 'text')
