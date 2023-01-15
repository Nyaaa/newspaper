from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post


@receiver(post_save, sender=Post)
def save_trigger(sender, instance, created, **kwargs):
    mails = []
    for cat in instance.category.all():
        emails = list(cat.subscribers.all().values_list('email', flat=True))
        if emails:
            mails += emails

    if mails:
        html_content = render_to_string('email_broadcast.html', {'post': instance})
        subject = f'NyankoNews: {instance.title} {instance.created.strftime("%d.%m.%Y")}'
        msg = EmailMultiAlternatives(
            subject=subject,
            body=instance.text,
            to=set(mails)
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(m2m_changed, sender=Post.category.through)
def m2m_trigger(sender, instance, action, **kwargs):
    """Without this code post_save gets no categories, since it's triggered before m2m field is saved"""
    if action == 'post_add':
        instance.save()
