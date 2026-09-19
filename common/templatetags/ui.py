from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def app_badge():
    # Libellé statique, entièrement maîtrisé côté serveur.
    return mark_safe('<span class="badge bg-info">auditflow</span>')
