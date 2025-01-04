<!--
 @since 2024.12.29, 19:24
 @changed 2024.12.30, 18:20
-->

# march-tales

March Tales django api and web frontend server.

## Build info (auto-generated)

- Project info: march-tales v.0.0.8 / 2025.01.05 00:47:09 +0300

## Resources

Repository: https://github.com/lilliputten/march-tales

Web page: https://tales.march.team

Django admin: https://tales.march.team/admin

## Project maintenance

### Python server (Django)

Use the poetry manager (requirements.txt + .venv + django manager.py on the server).

See `poetry-scripts` and `pyproject.toml` `[tool.poetry.scripts]` sectionfor refernce :

- `export_requirements` - Export `requirements.txt` from poetry dependecies.
- `django_migrate`
- `django_clean_db`
- `django_superuser`
- `django_runserver`
- `django_livereload`

### Webpack-based forntend part

Use pnpm commands (see `package.json`, `scripts` section`):

- `django-server`
- `clean-compiled`
- `django-reload-server`
- `dev`
- `build`
- `watch-build`

### Low-level maintenance utilities

Shell maintenance utilities are located in the `.utils` folder:

- `clean-all.sh`
- `increment-version.sh`
- `push-with-tags.sh`
- `update-build-variables.sh`
- `venv-init.sh`
