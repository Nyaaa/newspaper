from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
from django.utils import timezone


def my_job():
    today = timezone.now()
    posts = Post.objects.filter(created__range=[today - timezone.timedelta(days=7), today])
    subs = list(posts.values_list('category__subscribers__email', flat=True).distinct())
    subs = [i for i in subs if i != '' and i is not None]

    for sub in subs:
        to_send = []
        for post in posts:
            if sub in post.category.values_list('subscribers__email', flat=True).distinct():
                to_send.append(post)
        print(sub)
        print(to_send)

        html_content = render_to_string('weekly_broadcast.html', {'posts': to_send})
        msg = EmailMultiAlternatives(
            subject='NyankoNews Weekly Digest',
            to=[sub]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        print('done')

