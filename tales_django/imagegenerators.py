from imagekit import ImageSpec, register
from imagekit.processors import (
    ResizeToFit,
)

from tales_django.entities.Tracks.constants.preview_picture_sizes import (
    track_preview_picture_jpeg_quality,
    # track_preview_picture_thumb_size,
    track_small_image_thumb_size,
)


class small_image_thumb(ImageSpec):
    processors = (
        [
            ResizeToFit(track_small_image_thumb_size, track_small_image_thumb_size),
        ],
    )
    format = 'JPEG'
    options = {'quality': track_preview_picture_jpeg_quality}


register.generator('tales_django:small_image_thumb', small_image_thumb)
