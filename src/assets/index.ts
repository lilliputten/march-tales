/**
 * @desc Main entry point module (scripts)
 * @module src/assets/index.ts
 * @changed 2025.02.24, 22:12
 */

import { checkProjectVersion } from './checkProjectVersion';
import { initTracksPlayerWrapper } from './track-blocks/tracksPlayer';
import { initFloatingPlayer } from './entities/FloatingPlayer/floatingPlayer';
import { processTextContent } from './processTextContent';
import { initCookiesBanner } from './cookies-banner/cookiesBanner';

initCookiesBanner();

checkProjectVersion();
processTextContent();

initTracksPlayerWrapper();
initFloatingPlayer();
