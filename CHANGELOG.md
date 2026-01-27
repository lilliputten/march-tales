<!--
 @since 2025.03.19
 @changed 2026.01.27, 20:18
-->

# CHANGELOG

## [v.0.0.45](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.45) - 2026.01.27

Issue #89, Issue #88: Added i18n URL patterns and updated pages' meta tags

- Implemented i18n URL patterns (Issue #89): All localizable URLs are now wrapped with `i18n_patterns`, allowing localized prefixes like `/en/track/7`.
- Updated locale checking logic (Issue #89): The URL prefix now has the highest priority for locale detection.
- Updated Open Graph and Twitter meta tags (Issue #88): Enhanced social media previews and sharing capabilities.
- Added a default robots.txt file (Issue #88): Provides better control for search engine indexing.

These changes improve the site's internationalization support and overall web presence.

See also:

- [Issue #89: Allow to use locale url prefixes, like `/en/track/7`](https://github.com/lilliputten/march-tales/issues/89)
- [Issue #88: Add an opengraph images for shareable pages (tracks, authors, rubrics, mb, tags)](https://github.com/lilliputten/march-tales/issues/88)
- [Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.44...v.0.0.45)

## [v.0.0.44](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.44) - 2025.06.20

- Added content blocks model, admin panel & tag, some content blocks. Updated application page (added google play download link).
- Fixed a bug with cookies accept dialog (there was an invalid geometry updating algorithm).

See also:

- [Issue #86: Add ability to maintain user content blocks and strings](https://github.com/lilliputten/march-tales/issues/86)
- [Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.43...v.0.0.44)

## [v.0.0.43](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.43) - 2025.04.17

- Added `recents` api method.

See also:

- [Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.42...v.0.0.43)

## [v.0.0.42](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.42) - 2025.04.16

- Added yandex metrika counter.
- Updated cookie banner logic, added language cookie age parameter (to allow it to be saved for a longer time), yandex metrika is hidden for local dev server.

See also:

- [Issue #84: Add yandex metrica counter to the site](https://github.com/lilliputten/march-tales/issues/84)
- [Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.41...v.0.0.42)

## [v.0.0.41](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.41) - 2025.04.15

- [Issue #82](https://github.com/lilliputten/march-tales/issues/82): Added data synchronization on the server side and on the web client.

- Added client js triggers on login/logout, with cleaning data on logout and sending all the local data to sync on the server on log in. Added `logged-out` route and template.
- Server: Accepting timestamp values on track data update (favorite, played count, position).
- Added server-side user track update routine (`sync_user_tracks_api_view`)
- Updated client track controlling code (it allows multiple track nodes for the same track entity -- in different areas on the page).
- Added support for a local mysql database. Extracted user tracks' context to a dedicated module (should be used alongside track and favorites list contexts). Updated test fixtures' data.
- Client: Fixed a bug with empty local data but existed server ones.
- Client: Fixed open graph markup bugs.

See also:

- [Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.40...v.0.0.41)

## [v.0.0.40](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.40) - 2025.04.09

- [Issue #79](https://github.com/lilliputten/march-tales/issues/79): Added promo/stat section for the main page: it displays an information on recent/popular/random tracks.

See also:

- [Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.39...v.0.0.40)

## [v.0.0.39](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.39) - 2025.04.09

- [Issue #75](https://github.com/lilliputten/march-tales/issues/75): Added synchronization of playback positions on the web clients: if the last played timestamp from the server is newer than local one, then the server playback position is used, if presented.

See also:

- [Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.38...v.0.0.39)

## [v.0.0.38](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.38) - 2025.03.28

- [Issue #74](https://github.com/lilliputten/march-tales/issues/74): Added editable flat pages (via overriden `django.contrib.flatpages`).
- Added flatpage module workarounds. Used overriden ewxposed modules (`tales_django/entities/flatpages`: ). A settings parameter `FLATPAGE_CONTEXT_GETTER` to pass a context to the template. Added settings parameter `FLATPAGE_DEFAULT_TEMPLATE` to specify default flat pages' template.
- Added `ckeditor` module to allow rich text content editor.
- Extended `FlatPage` data model to allow content translation.
- Fixed search issues (filter only unique results, added search by author and rubrics)
- Added flatpages context getter and core template.
- Added flat pages `about` and `application` (with crsp templates).
- Added a forced language parameter (`?hl=ru`).

See also:

- [Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.37...v.0.0.38)

## [v.0.0.37](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.37) - 2025.03.28

- [Issue #71](https://github.com/lilliputten/march-tales/issues/71): Added detailed footer.
- [Issue #69](https://github.com/lilliputten/march-tales/issues/69): Added an `application` page with two-language content and previews gallery (with translated captions).
- Added `slick-carousel-1.8.1` (with static vendor library, templates, styles and typescript code).
- Unified thumbnails usage logic (always with a `thumbs` subpath), created a template tag to automatically generate a thumbnail image file name (and url) from the source one.

See also:

- [Compare with the previous version](https://github.com/lilliputten/march-tales/compare/v.0.0.35...v.0.0.37)

## [v.0.0.35](https://github.com/lilliputten/march-tales/releases/tag/v.0.0.35) - 2025.03.23

- Added support of LQIP image placeholders (see `media_files_encoder` template tag), using a tag generator `lqip_media_img_tag`, see example in `big-tracks-list-item` template. Added `imagekit` package to support image processing, added a few of different options for Track's `preview_picture`.
- Using short github version tag notation.

See also:

- [Compare with the previous version](https://github.com/lilliputten/march-tales/compare/march-tales-v.0.0.34...v.0.0.35)

## [v.0.0.34](https://github.com/lilliputten/march-tales/tree/march-tales-v.0.0.34) - 2025.03.19

The first 'public' version.
