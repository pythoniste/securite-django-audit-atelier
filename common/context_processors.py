from django.conf import settings


def cdn(request):
    return {"CDN_BASE": settings.CDN_BASE}
