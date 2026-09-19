# auditflow — application d'entraînement à l'audit de sécurité

> ⚠️ **AVERTISSEMENT** — Cette application contient des failles de sécurité
> **volontaires**. Elle est destinée **exclusivement** à un usage pédagogique
> en environnement isolé (poste local, réseau de formation).
> **Ne jamais l'exposer sur Internet, ni la déployer en production, ni la
> connecter à des données réelles.**

Mini-SaaS de facturation et notes de frais B2B, servant de support à un
exercice d'audit progressif (3 livrets, difficulté croissante).

## Démarrage rapide

```bash
make venv
make migrate                 # base SQLite par défaut
make seed
make run-runserver           # http://localhost:8000
```

## Matrice serveur × base de données

```bash
make run-gunicorn                          # gunicorn nu
make migrate DB_ENGINE=postgres            # après: docker compose --profile postgres up -d
make migrate DB_ENGINE=mysql               # après: docker compose --profile mysql up -d
```

Certaines failles ne se manifestent que sous une combinaison précise
(serveur ou moteur de base). C'est voulu.

## Pour les apprenants

Vous recevez un ou plusieurs **livrets** (PDF). Chacun vous oriente vers des
zones à auditer, sans nommer les fichiers. Remplissez la **grille de
restitution** fournie. Le corrigé est remis en fin de session.

## Comptes de démonstration

Fournis par `make seed` (voir la sortie de la commande).
