print('imports...')
from news.models import *

print('creating users...')
u1 = User.objects.create_user('user01')
u2 = User.objects.create_user('user02')

a1 = Author.objects.create(user=u1)
a2 = Author.objects.create(user=u2)

print('creating data...')
ct1 = Category.objects.create(name='Facepalm')
ct2 = Category.objects.create(name='Awww')
ct3 = Category.objects.create(name='LOL')
ct4 = Category.objects.create(name='Nope')

p1 = Post.objects.create(author=a1, type=Post.PostType.ARTICLE, title='Test article #1', text='Suspendisse tristique est faucibus magna commodo condimentum. Duis sodales enim vel neque scelerisque volutpat. Nunc in ligula purus. Curabitur molestie arcu vel ultricies mattis. Proin dolor ex, ultricies ac ullamcorper sit amet, malesuada eu purus. Cras nec dapibus eros. Aenean volutpat augue ante. Sed vulputate varius pulvinar. Ut sed tempus augue. Praesent accumsan urna tortor. Nunc porttitor nisl leo. Donec aliquam nisl eget velit egestas, in tempor nunc tempus. Donec feugiat malesuada bibendum.')
p2 = Post.objects.create(author=a2, type=Post.PostType.ARTICLE, title='Test article #2', text='Donec pulvinar purus odio, non placerat nisi volutpat ac. Duis in varius magna. Phasellus nec sagittis eros, non accumsan est. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Proin suscipit tempor libero non mattis. Donec consequat sagittis est in laoreet. Sed sagittis nibh sem, eu tempor massa sollicitudin sit amet. Morbi posuere arcu ac metus laoreet efficitur.')
p3 = Post.objects.create(author=a1, title='Test news piece #1', text='Nunc egestas purus ut enim tincidunt, a ultricies arcu condimentum. Mauris vel suscipit nibh. Nam dui ligula, auctor et finibus quis, rhoncus in urna. Vestibulum consectetur tellus suscipit, volutpat massa quis, bibendum ante. Nunc ultricies sed est sed tincidunt. Cras nec velit in erat ultricies facilisis. In dolor lorem, lobortis vitae turpis et, fermentum lacinia sapien. Suspendisse justo massa, suscipit at quam at, elementum aliquam turpis. Pellentesque et vestibulum justo, eget dapibus lacus. Sed vitae tempus urna, sed convallis dolor.')

p1.category.add(ct1)
p2.category.add(ct2, ct3)
p3.category.add(ct3, ct4)

c1 = Comment.objects.create(post=p1, user=u1, text='comment01')
c2 = Comment.objects.create(post=p2, user=u1, text='comment02')
c3 = Comment.objects.create(post=p3, user=u2, text='comment03')
c4 = Comment.objects.create(post=p1, user=u1, text='comment04')
c5 = Comment.objects.create(post=p2, user=u2, text='comment05')

p1.like()
p2.like()
p2.like()
p3.like()
c1.dislike()
c2.like()
c3.like()
c4.like()
c5.dislike()

a1.update_rating()
a2.update_rating()

print('Top author:', Author.objects.all().order_by('_rating').values('user__username', '_rating').last())
print('Top article:', Post.objects.filter(type=Post.PostType.ARTICLE).order_by('rating').values('created', 'author__user__username', 'rating', 'title').last())
top_post = Post.objects.filter(type=Post.PostType.ARTICLE).order_by('rating').last()
print('Text preview:', top_post.preview())
print('Comments:', Comment.objects.filter(post=top_post).values('created', 'user__username', 'rating', 'text'))
print('Done')
