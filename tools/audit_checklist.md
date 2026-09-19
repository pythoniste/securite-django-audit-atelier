# Méthode d'audit — fiche réutilisable

Objectif : une démarche reproductible, pas une chasse au trésor. À appliquer
dans cet ordre sur toute base Django.

## 1. Ce que Django dit tout seul
```bash
python manage.py check --deploy
```
Chaque `security.Wxxx` est une piste. Comprenez ce que chacun protège.

## 2. Motifs à rechercher (odeurs de code)
Chaque motif n'est pas une faille en soi : c'est un point à **justifier**.
```bash
grep -rnE "\|safe|mark_safe|format_html" templates/ **/*.py   # échappement
grep -rn  "csrf_exempt" .                                     # CSRF
grep -rnE "\.raw\(|\.extra\(|cursor\(\)|\.execute\(" .        # SQL
grep -rn  "fields *= *['\"]__all__['\"]" .                    # mass assignment
grep -rnE "pickle|yaml.load\(|eval\(|os.system|subprocess" . # exécution
grep -rn  "requests.get\(|urlopen\(" .                        # SSRF
grep -rn  "get_object_or_404" .                               # contrôle d'accès objet
```

## 3. Dépendances et statique
```bash
pip-audit -r requirements.txt      # CVE connues
bandit -r . -x .venv               # analyse statique
```

## 4. En-têtes réellement émis (selon le serveur)
```bash
curl -sI http://127.0.0.1:8000/ | grep -iE 'referrer|x-frame|content-type-options|strict-transport'
```
Comparez gunicorn nu vs Apache/nginx : un en-tête posé par le serveur
**disparaît** si l'on change de mode de lancement.

## 5. Revue manuelle (ce qu'aucun outil ne trouve)
- **Autorisation** : chaque `get()` / `filter()` est-il restreint au périmètre
  de l'utilisateur (société, propriétaire) ? L'absence de filtre = IDOR.
- **Uploads** : type, extension et **chemin** de destination validés ?
- **Redirections** : `next`/`url` validés par `url_has_allowed_host_and_scheme` ?
- **Logique métier** : transitions d'état vérifiées côté serveur ?
- **Secrets** : présents dans le dépôt ou son historique (`git log -p`) ?
- **Ressources tierces** : chargées avec SRI ? sous quelle CSP ?

## 6. Restitution
Une ligne par constat : fichier, ligne, classe (OWASP), risque, correction.
Signalez aussi les **faux positifs** (un motif suspect mais sain) : savoir
écarter est aussi important que savoir trouver.
