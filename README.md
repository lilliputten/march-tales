<!--
 @since 2025.03.14, 22:00
 @changed 2025.03.14, 22:00
-->

# march-tales

March Tales django api and web frontend server.

## Build info (auto-generated)

- Project info: march-tales v.0.0.34 / 2025.03.19 06:53:35 +0300

## Resources

Repository: https://github.com/lilliputten/march-tales

Web page: https://tales.march.team

Django admin: https://tales.march.team/admin

## Project maintenance

### Installation

For development:

- Unpack all the zip archives under `static/vendor` folder first.
- Create mock (or copy from real flutter project) mobile application artifacts under `static/downloads/apk` folder. These should be `output-metadata.json` and `*.apk` files, by default. (See sample fake files in the folder.)

### Python server (Django)

Use the poetry manager (requirements.txt + .venv + django manager.py on the server).

See `poetry-scripts` and `pyproject.toml` `[tool.poetry.scripts]` sectionfor refernce :

- `export_requirements` - Export `requirements.txt` from poetry dependecies.
- `django_migrate`
- `django_clean_db`
- `django_superuser`
- `django_runserver`
- `django_livereload`

Don't forget to export requirements (from the poetry project a to plain `requirements.txt` file) after dependencies updates.

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
