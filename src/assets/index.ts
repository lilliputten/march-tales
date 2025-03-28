/**
 * @desc Main entry point module (scripts)
 * @module src/assets/index.ts
 * @changed 2025.03.28, 03:34
 */

import { checkProjectVersion } from './checkProjectVersion';
import { initTracksPlayerWrapper } from './track-blocks/tracksPlayer';
import { initFloatingPlayer } from './entities/FloatingPlayer/floatingPlayer';
import { processTextContent } from './processTextContent';
import { initCookiesBanner } from './cookies-banner/cookiesBanner';
import { initCarousels } from './carousel/carousels';
import { initAOS } from './aos';

initCookiesBanner();

checkProjectVersion();
processTextContent();

initTracksPlayerWrapper();
initFloatingPlayer();

initCarousels();
initAOS();
