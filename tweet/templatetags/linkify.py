import re
from django import template

register = template.Library()

@register.filter()
def linkify(text):
    url_regex = r'(https?://[^\s]+)'
    return re.sub(url_regex, r'<a href="\1" class="text-blue-500 underline" target="_blank">\1</a>', text)
