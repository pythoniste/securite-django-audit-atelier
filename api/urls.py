from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("users", views.UserViewSet)
router.register("invoices", views.InvoiceViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("quick-status/", views.quick_status, name="quick_status"),
    path("webhook/", views.webhook, name="webhook"),
    path("by-status/", views.invoices_by_status, name="by_status"),
]
