# Déploiement — deux modes

Le même code se lance de deux façons, et **la posture de sécurité n'est pas la même** :

| Mode | Commande | En-têtes de sécurité |
|------|----------|----------------------|
| gunicorn nu | `make run-gunicorn` | ceux que pose l'application Django |
| Apache → gunicorn | vhost `apache-auditflow.conf` | ceux d'Apache **en plus** |

Comparez :

```bash
make run-gunicorn &
curl -sI http://localhost:8000/ | grep -iE 'referrer-policy|x-frame|content-type-options'
```

puis les mêmes en-têtes derrière Apache. La différence est le cœur d'une des failles.
