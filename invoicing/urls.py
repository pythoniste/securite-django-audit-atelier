from django.urls import path

from . import views

app_name = "invoicing"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("invoices/", views.invoice_list, name="invoice_list"),
    path("invoices/new/", views.invoice_create, name="invoice_create"),
    path("invoices/<int:pk>/", views.invoice_detail, name="invoice_detail"),
    path("report/", views.report, name="report"),
    path("export/", views.export_csv, name="export_csv"),
    path("stats/", views.stats, name="stats"),
    path("expenses/", views.expense_list, name="expense_list"),
    path("expenses/<int:pk>/reimburse/", views.expense_reimburse, name="expense_reimburse"),
    path("expenses/<int:pk>/transition/", views.expense_transition, name="expense_transition"),
    path("expenses/<int:pk>/receipt/", views.upload_receipt, name="upload_receipt"),
    path("htmx/clients/", views.client_search, name="client_search"),
    path("htmx/projects/", views.project_options, name="project_options"),
]
