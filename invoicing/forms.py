from django import forms

from .models import Client, Invoice, InvoiceLine


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["number", "client", "status", "description"]

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["client"].queryset = Client.objects.filter(company=company)


# Les lignes de facture ; le prix unitaire est saisi avec la ligne.
InvoiceLineFormSet = forms.inlineformset_factory(
    Invoice,
    InvoiceLine,
    fields=["label", "quantity", "unit_price"],
    extra=1,
    can_delete=True,
)
