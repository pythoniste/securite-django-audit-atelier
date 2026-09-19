from django.shortcuts import get_object_or_404, render

from .models import ShareLink


def shared_note(request, token):
    share = get_object_or_404(ShareLink, token=token)
    note = share.expense
    return render(request, "sharing/shared_note.html", {"note": note, "share": share})
