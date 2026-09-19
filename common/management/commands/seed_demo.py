from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import Company, Membership
from invoicing.models import Client, ExpenseNote, Invoice, InvoiceLine, Project
from sharing.models import ShareLink


class Command(BaseCommand):
    help = "Charge des données de démonstration (idempotent)."

    def handle(self, *args, **options):
        ShareLink.objects.all().delete()
        InvoiceLine.objects.all().delete()
        ExpenseNote.objects.all().delete()
        Invoice.objects.all().delete()
        Project.objects.all().delete()
        Client.objects.all().delete()
        Membership.objects.all().delete()
        Company.objects.all().delete()
        User.objects.filter(username__in=["alice", "charlie", "bob", "root"]).delete()

        acme = Company.objects.create(name="Acme SARL", siret="12345678900011")
        globex = Company.objects.create(name="Globex SA", siret="99999999900099")

        def member(username, email, company, role):
            user = User.objects.create_user(username, email, "Password123")
            Membership.objects.create(user=user, company=company, role=role)
            return user

        alice = member("alice", "alice@acme.example", acme, "admin")
        charlie = member("charlie", "charlie@acme.example", acme, "member")
        bob = member("bob", "bob@globex.example", globex, "admin")
        User.objects.create_superuser("root", "root@auditflow.local", "rootpwd")

        ca = Client.objects.create(company=acme, name="Client Alpha", email="alpha@client.example")
        cg = Client.objects.create(company=globex, name="Client Gamma", email="gamma@client.example")
        Project.objects.create(company=acme, client=ca, name="Site vitrine")
        Project.objects.create(company=globex, client=cg, name="Projet confidentiel Globex")

        inv = Invoice.objects.create(
            company=acme, client=ca, number="2026-0001", status="sent",
            description="<p>Prestation de conseil</p>", created_by=alice,
        )
        InvoiceLine.objects.create(invoice=inv, label="Audit", quantity=2, unit_price=500)
        InvoiceLine.objects.create(invoice=inv, label="Formation", quantity=1, unit_price=1200)
        Invoice.objects.create(
            company=acme, client=ca, number="2026-0002", status="draft",
            description="Note interne <script>alert(document.cookie)</script>",
            created_by=charlie,
        )
        Invoice.objects.create(
            company=globex, client=cg, number="2026-0009", status="paid", created_by=bob
        )

        ExpenseNote.objects.create(
            company=acme, user=charlie, label="Train Paris-Lyon", amount="89.90", status="submitted"
        )
        note = ExpenseNote.objects.create(
            company=globex, user=bob, label="Hôtel (données RH)", amount="240.00", status="approved"
        )
        share = ShareLink.objects.create(expense=note)

        self.stdout.write(self.style.SUCCESS("Données de démonstration chargées."))
        self.stdout.write("Comptes (mot de passe = Password123) :")
        self.stdout.write("  alice   — admin Acme")
        self.stdout.write("  charlie — membre Acme")
        self.stdout.write("  bob     — admin Globex")
        self.stdout.write("  root    — superuser Django (mot de passe: rootpwd)")
        self.stdout.write(f"Lien de partage (URL-capacité) : /s/{share.token}/note/")
