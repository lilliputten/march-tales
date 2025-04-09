default_preview_jpeg_quality = 70

micro_image_thumb_size = 8
small_image_thumb_size = 32

track_small_image_thumb_size = small_image_thumb_size

track_preview_picture_full_size = 600
track_preview_picture_small_size = 85
track_preview_picture_thumb_size = round(track_preview_picture_full_size / 10)
track_preview_picture_jpeg_quality = default_preview_jpeg_quality

author_portrait_picture_full_size = 150
author_portrait_picture_thumb_size = round(author_portrait_picture_full_size / 10)
author_portrait_picture_jpeg_quality = default_preview_jpeg_quality

__all__ = [
    'track_preview_picture_full_size',
    'track_preview_picture_small_size',
    'track_preview_picture_thumb_size',
    'track_preview_picture_jpeg_quality',
    'author_portrait_picture_full_size',
    'author_portrait_picture_thumb_size',
    'author_portrait_picture_jpeg_quality',
]
