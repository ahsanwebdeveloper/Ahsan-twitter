# myapp/templatetags/custom_filters.py
from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()

class _Match:
    def __init__(self, start, end, url):
        self.index = start
        self.last_index = end
        self.url = url

class LinkifyItFallback:
    URL_RE = re.compile(r'(?i)\b((?:https?://|www\.)[^\s<>"]+)', re.UNICODE)

    def match(self, text):
        matches = []
        for m in self.URL_RE.finditer(text):
            url = m.group(0)
            # normalize URLs that start with "www."
            if url.startswith('www.'):
                url = 'http://' + url
            matches.append(_Match(m.start(), m.end(), url))
        return matches

linkify = LinkifyItFallback()

@register.filter
def linkify_text(value):
    matches = linkify.match(value)
    if not matches:
        return value
    html = ""
    last_index = 0
    for m in matches:
        start, end = m.index, m.last_index
        html += value[last_index:start]
        html += f'<a href="{m.url}" target="_blank" class="text-blue-400 underline">{m.url}</a>'
        last_index = end
    html += value[last_index:]
    return mark_safe(html)
