from django import template
import re


register = template.Library()

CENSOR_LIST = ['profanity_test', 'ass']


@register.filter()
def censor(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError('Censor input must be a string')

    for word in CENSOR_LIST:
        text = re.sub(r"\b" + f"({word[0]}){word[1:]}" + r"\b",
                      lambda x, w=word: (w[0].upper() if x.group(1).isupper() else w[0]) + f"{'*' * (len(w) - 1)}",
                      text,
                      flags=re.IGNORECASE)
    return text

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()
