from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post


@receiver(post_save, sender=Post)  # FIXME m2m empty on creation
def post_email_broadcast(sender, instance, created, **kwargs):
    print('save')
    html_content = render_to_string('email_broadcast.html', {'post': instance})
    if created:
        subject = f'New post: {instance.title} {instance.created.strftime("%d.%m.%Y")}'
    else:
        subject = f'Post updated: {instance.title} {instance.created.strftime("%d.%m.%Y")}'

    mails = []
    for cat in instance.category.all():
        emails = list(cat.subscribers.all().values_list('email', flat=True))
        if emails:
            mails.append(*emails)

    print(instance.category.all(), instance.title, instance.author)
    print(mails)
    msg = EmailMultiAlternatives(
        subject=subject,
        body=instance.text,
        to=mails
    )
    msg.attach_alternative(html_content, "text/html")
    # msg.send()


@receiver(m2m_changed, sender=Post.category.through)
def m2m_trigger(sender, instance, **kwargs):
    print('m2m')
    mails = []
    for cat in instance.category.all():
        emails = list(cat.subscribers.all().values_list('email', flat=True))
        if emails:
            mails.append(*emails)

    print(instance.category.all(), instance.title, instance.author)
    print(mails)

