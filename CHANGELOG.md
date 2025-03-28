<!--
 @since 2025.03.19
 @changed 2025.03.28, 06:19
-->

# CHANGELOG

## [v.0.0.37](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.37) - 2025.03.28

- [Issue #71](https://github.com/lilliputten/march-tales/issues/71) Added detailed footer.
- [Issue #69](https://github.com/lilliputten/march-tales/issues/69): Added an `application` page with two-language content and previews gallery (with translated captions).
- Added `slick-carousel-1.8.1` (with static vendor library, templates, styles and typescript code).
- Unified thumbnails usage logic (always with a `thumbs` subpath), created a template tag to automatically generate a thumbnail image file name (and url) from the source one.

[Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.35...v.0.0.37)

## [v.0.0.35](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.35) - 2025.03.23

- Added support of LQIP image placeholders (see `media_files_encoder` template tag), using a tag generator `lqip_media_img_tag`, see example in `big-tracks-list-item` template. Added `imagekit` package to support image processing, added a few of different options for Track's `preview_picture`.
- Using short github version tag notation.

[Compare with the previous version](https://github.com/lilliputten/march-tales/compare/march-tales-v.0.0.34...v.0.0.35)

## [0.0.34](https://github.com/lilliputten/march-tales/tree/march-tales-v.0.0.34) - 2025.03.19

The first 'public' version.
