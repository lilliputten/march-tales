# Flatpages app overrides

Added parameters that allow to pass a context to the template and provide a default template from settings:

Added the following settings parameters:

- `FLATPAGE_CONTEXT_GETTER` to pass a context to the template renderer.
- `FLATPAGE_DEFAULT_TEMPLATE` to specify default flatpage template.

The changes are in the `views.py` module.

The others (`middleware.py` and `urls.py`) supposed only to support these fixes.

See a PR in the Django code base:

- [Added flatpages app parameters to pass a context and set a default template](https://github.com/django/django/pull/19344)
