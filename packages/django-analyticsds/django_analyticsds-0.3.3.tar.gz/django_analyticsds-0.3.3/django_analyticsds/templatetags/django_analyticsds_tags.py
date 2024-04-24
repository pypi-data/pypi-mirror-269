from django.template import Library, loader
from _data import analyticsds

register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


@register.simple_tag(takes_context=True)
def make_analytics(context):
    c = analyticsds.context
    t = loader.get_template(f"django_analyticsds/analyticsds.html")
    context.update(c)
    return t.render(context.flatten())
