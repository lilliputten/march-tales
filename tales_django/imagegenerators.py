from imagekit import ImageSpec, register
from imagekit.processors import (
    ResizeToFit,
)

from tales_django.entities.Tracks.constants.preview_picture_sizes import (
    track_preview_picture_jpeg_quality,
    track_preview_picture_thumb_size,
)


class preview_picture_thumb(ImageSpec):
    processors = (
        [
            ResizeToFit(track_preview_picture_thumb_size, track_preview_picture_thumb_size),
        ],
    )
    format = 'JPEG'
    options = {'quality': track_preview_picture_jpeg_quality}


register.generator('tales_django:preview_picture_thumb', preview_picture_thumb)
