"""Configuration gunicorn de démonstration."""
bind = "0.0.0.0:8000"
workers = 3
timeout = 60
accesslog = "logs/access.log"
errorlog = "logs/error.log"
# Format d'accès : journalise la requête complète (chemin + query).
access_log_format = '%(h)s "%(r)s" %(s)s %(b)s "%(a)s"'
