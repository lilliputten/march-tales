<!--
 @since 2025.03.19
 @changed 2025.04.15, 15:59
-->

# CHANGELOG

## [v.0.0.41](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.41) - 2025.04.15

- [Issue #82](https://github.com/lilliputten/march-tales/issues/82): Added data synchronization on the server side and on the web client.

- Added client js triggers on login/logout, with cleaning data on logout and sending all the local data to sync on the server on log in. Added `logged-out` route and template.
- Server: Accepting timestamp values on track data update (favorite, played count, position).
- Added server-side user track update routine (`sync_user_tracks_api_view`)
- Updated client track controlling code (it allows multiple track nodes for the same track entity -- in different areas on the page).
- Added support for a local mysql database. Extracted user tracks' context to a dedicated module (should be used alongside track and favorites list contexts). Updated test fixtures' data.
- Client: Fixed a bug with empty local data but existed server ones.
- Client: Fixed open graph markup bugs.

## [v.0.0.41](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.41) - 2025.04.13

- [Issue #82](https://github.com/lilliputten/march-tales/issues/82): Added data synchronization on the server side and on the web client.

- Added client js triggers on login/logout, with cleaning data on logout and sending all the local data to sync on the server on log in. Added `logged-out` route and template.
- Server: Accepting timestamp values on track data update (favorite, played count, position).
- Added server-side user track update routine (`sync_user_tracks_api_view`)
- Updated client track controlling code (it allows multiple track nodes for the same track entity -- in different areas on the page).
- Added support for a local mysql database. Extracted user tracks' context to a dedicated module (should be used alongside track and favorites list contexts). Updated test fixtures' data.
- Client: Fixed a bug with empty local data but existed server ones.

[Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.40...v.0.0.41)

## [v.0.0.40](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.40) - 2025.04.09

- [Issue #79](https://github.com/lilliputten/march-tales/issues/79): Added promo/stat section for the main page: it displays an information on recent/popular/random tracks.

[Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.39...v.0.0.40)

## [v.0.0.39](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.39) - 2025.04.09

- [Issue #75](https://github.com/lilliputten/march-tales/issues/75): Added synchronization of playback positions on the web clients: if the last played timestamp from the server is newer than local one, then the server playback position is used, if presented.

[Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.38...v.0.0.39)

## [v.0.0.38](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.38) - 2025.03.28

- [Issue #74](https://github.com/lilliputten/march-tales/issues/74): Added editable flat pages (via overriden `django.contrib.flatpages`).
- Added flatpage module workarounds. Used overriden ewxposed modules (`tales_django/entities/flatpages`: ). A settings parameter `FLATPAGE_CONTEXT_GETTER` to pass a context to the template. Added settings parameter `FLATPAGE_DEFAULT_TEMPLATE` to specify default flat pages' template.
- Added `ckeditor` module to allow rich text content editor.
- Extended `FlatPage` data model to allow content translation.
- Fixed search issues (filter only unique results, added search by author and rubrics)
- Added flatpages context getter and core template.
- Added flat pages `about` and `application` (with crsp templates).
- Added a forced language parameter (`?hl=ru`).

[Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.37...v.0.0.38)

## [v.0.0.37](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.37) - 2025.03.28

- [Issue #71](https://github.com/lilliputten/march-tales/issues/71): Added detailed footer.
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
