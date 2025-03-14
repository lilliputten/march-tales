from django.core.validators import EMPTY_VALUES
from django.template.loaders.filesystem import Loader as FilesystemLoader
from django.template.utils import get_app_template_dirs
from django.urls import Resolver404, resolve

from tales_django.middleware.CurrentRequestMiddleware import thread_data

# from tales_django.middleware import _thread_data


class UnfoldAdminLoader(FilesystemLoader):
    def _has_unfold_dir(self, template_dir):
        request = getattr(thread_data, 'request', None)

        if not request or request.path in EMPTY_VALUES:
            return False

        request_path = request.path
        namespaces = resolve(request_path).namespaces

        try:
            if 'admin' in namespaces:
                iter = template_dir.iterdir()
                for dir in iter:
                    if dir.name == 'unfold':
                        return True
        except Resolver404:
            pass

        return False

    def get_dirs(self):
        template_dirs = []

        app_template_dirs = get_app_template_dirs('templates')
        for template_dir in app_template_dirs:
            # template_dir_str = str(template_dir)
            # if 'unfold' in template_dir_str:
            #     continue
            if self._has_unfold_dir(template_dir):
                continue
            # template_dirs.append(template_dir)

        return template_dirs
