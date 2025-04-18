from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit

from tales_django.entities.Tracks.constants.preview_picture_sizes import (
    default_preview_jpeg_quality,
    micro_image_thumb_size,
    track_small_image_thumb_size,
)


class micro_image_thumb(ImageSpec):
    processors = (
        [
            ResizeToFit(micro_image_thumb_size, micro_image_thumb_size),
        ],
    )
    format = 'JPEG'
    options = {'quality': default_preview_jpeg_quality}


register.generator('tales_django:micro_image_thumb', micro_image_thumb)


class small_image_thumb(ImageSpec):
    processors = (
        [
            ResizeToFit(track_small_image_thumb_size, track_small_image_thumb_size),
        ],
    )
    format = 'JPEG'
    options = {'quality': default_preview_jpeg_quality}


register.generator('tales_django:small_image_thumb', small_image_thumb)
