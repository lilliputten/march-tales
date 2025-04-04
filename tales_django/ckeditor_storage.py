import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class ckeditor_storage(FileSystemStorage):
    """Custom storage for django_ckeditor_5 images."""

    location = os.path.join(settings.MEDIA_ROOT, 'ckeditor')
    base_url = urljoin(settings.MEDIA_URL, 'ckeditor/')
