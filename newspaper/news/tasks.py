from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Author
from django.utils import timezone
import logging
from celery import shared_task

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@shared_task
def broadcast():
    today = timezone.now()
    posts = Post.objects.filter(created__range=[today - timezone.timedelta(days=7), today])
    subs = list(posts.values_list('category__subscribers__email', flat=True).distinct())
    subs = [i for i in subs if i != '' and i is not None]

    for sub in subs:
        to_send = [post for post in posts if sub in
                   post.category.values_list('subscribers__email', flat=True).distinct()]
        logger.info(f'sending to: {sub}')
        logger.info(f'sending posts: {to_send}')

        html_content = render_to_string('weekly_broadcast.html', {'posts': to_send})
        msg = EmailMultiAlternatives(
            subject='NyankoNews Weekly Digest',
            to=[sub]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def notification(pk):
    post = Post.objects.get(id=pk)
    mails = []
    for cat in post.category.all():
        emails = list(cat.subscribers.all().values_list('email', flat=True))
        if emails:
            mails += emails

    if mails:
        html_content = render_to_string('email_broadcast.html', {'post': post})
        subject = f'NyankoNews: {post.title} {post.created.strftime("%d.%m.%Y")}'
        msg = EmailMultiAlternatives(
            subject=subject,
            body=post.text,
            to=set(mails)
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def update_authors_rating():
    authors = Author.objects.all()
    for author in authors:
        author.update_rating()

