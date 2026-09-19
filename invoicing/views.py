import csv

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models.expressions import RawSQL
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import Company

from .forms import InvoiceForm, InvoiceLineFormSet
from .models import Client, ExpenseNote, Invoice, Project


def _company(request):
    membership = getattr(request.user, "membership", None)
    return membership.company if membership else None


@login_required
def dashboard(request):
    company = _company(request)
    if company:
        invoices = Invoice.objects.filter(company=company)
        expenses = ExpenseNote.objects.filter(company=company)
    else:
        invoices = Invoice.objects.none()
        expenses = ExpenseNote.objects.none()
    return render(
        request,
        "invoicing/dashboard.html",
        {"company": company, "invoices": invoices, "expenses": expenses},
    )


@login_required
def invoice_list(request):
    company = _company(request)
    qs = Invoice.objects.filter(company=company)
    number = request.GET.get("number", "")
    if number:
        qs = qs.extra(where=[f"number = '{number}'"])
    sort = request.GET.get("sort", "number")
    qs = qs.extra(order_by=[sort])
    return render(
        request,
        "invoicing/invoice_list.html",
        {"invoices": qs, "number": number, "sort": sort},
    )


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, "invoicing/invoice_detail.html", {"invoice": invoice})


@login_required
def invoice_create(request):
    company = _company(request)
    if request.method == "POST":
        form = InvoiceForm(request.POST, company=company)
        formset = InvoiceLineFormSet(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.company = company
            invoice.created_by = request.user
            invoice.save()
            formset = InvoiceLineFormSet(request.POST, instance=invoice)
            if formset.is_valid():
                formset.save()
                return redirect("invoicing:invoice_detail", pk=invoice.pk)
    else:
        form = InvoiceForm(company=company)
        formset = InvoiceLineFormSet()
    return render(
        request, "invoicing/invoice_form.html", {"form": form, "formset": formset}
    )


@login_required
def report(request):
    q = request.GET.get("q", "")
    sql = f"SELECT * FROM invoicing_invoice WHERE number LIKE '%{q}%'"
    invoices = list(Invoice.objects.raw(sql))
    return render(request, "invoicing/report.html", {"invoices": invoices, "q": q})


@login_required
def export_csv(request):
    status = request.GET.get("status", "draft")
    sql = (
        "SELECT number, status, description FROM invoicing_invoice "
        "WHERE status = '" + status + "'"
    )
    with connection.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = "attachment; filename=invoices.csv"
    writer = csv.writer(resp)
    writer.writerow(["number", "status", "description"])
    writer.writerows(rows)
    return resp


@login_required
def stats(request):
    year = request.GET.get("year", "2026")
    companies = Company.objects.annotate(
        n_invoices=RawSQL(
            "(SELECT COUNT(*) FROM invoicing_invoice "
            "WHERE company_id = accounts_company.id "
            f"AND number LIKE '{year}%')",
            [],
        )
    )
    return render(request, "invoicing/stats.html", {"companies": companies, "year": year})


@login_required
def expense_list(request):
    company = _company(request)
    expenses = ExpenseNote.objects.filter(company=company)
    return render(request, "invoicing/expense_list.html", {"expenses": expenses})


@login_required
def expense_reimburse(request, pk):
    note = get_object_or_404(ExpenseNote, pk=pk)
    if note.status != "reimbursed":
        note.status = "reimbursed"
        note.reimbursed_at = timezone.now()
        note.save()
        # Déclenchement du virement au bénéficiaire.
    return redirect("invoicing:expense_list")


@login_required
def expense_transition(request, pk):
    note = get_object_or_404(ExpenseNote, pk=pk)
    if request.method == "POST":
        note.status = request.POST.get("status", note.status)
        note.save()
    return redirect("invoicing:expense_list")


@login_required
def client_search(request):
    q = request.GET.get("q", "")
    company = _company(request)
    clients = Client.objects.filter(company=company, name__icontains=q)[:10]
    items = "".join(f"<li>{c.name}</li>" for c in clients)
    html = f'<div class="results">Résultats pour « {q} »</div><ul>{items}</ul>'
    return HttpResponse(html)


@login_required
def project_options(request):
    client_id = request.GET.get("client", "")
    projects = Project.objects.filter(client_id=client_id)
    return render(
        request, "partials/project_options.html", {"projects": projects}
    )


@login_required
def upload_receipt(request, pk):
    import os

    from django.conf import settings

    note = get_object_or_404(ExpenseNote, pk=pk)
    if request.method == "POST" and request.FILES.get("receipt"):
        upload = request.FILES["receipt"]
        name = request.POST.get("name") or upload.name
        base = os.path.join(settings.MEDIA_ROOT, "receipts")
        os.makedirs(base, exist_ok=True)
        dest = os.path.join(base, name)
        with open(dest, "wb") as out:
            for chunk in upload.chunks():
                out.write(chunk)
        note.receipt = f"receipts/{name}"
        note.save()
        return redirect("invoicing:expense_list")
    return render(request, "invoicing/receipt_upload.html", {"note": note})
