# Demo data fixtures

To install test data (for local testting), use:

```bash
python manage.py loaddata site-local test-users
```

To quickly remove migrations and dev.time db, use:

```bash
rm -Rvf tales_django/migrations/* db.sqlite3 && touch tales_django/migrations/__init__.py
```

or use env script:

```bash
sh .scripts/django-reset-db.sh
```
