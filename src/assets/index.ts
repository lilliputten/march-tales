/**
 * @desc Main entry point module (scripts)
 * @module src/assets/index.ts
 * @changed 2025.04.12, 23:23
 */

import { userSession } from './userSession';
import { checkProjectVersion } from './checkProjectVersion';
import { initTracksPlayerWrapper } from './track-blocks/tracksPlayer';
import { initFloatingPlayer } from './entities/FloatingPlayer/floatingPlayer';
import { processTextContent } from './processTextContent';
import { initCookiesBanner } from './cookies-banner/cookiesBanner';
import { initCarousels } from './carousel/carousels';
import { initAOS } from './aos';

initCookiesBanner();
processTextContent();
checkProjectVersion();
userSession();

initTracksPlayerWrapper();
initFloatingPlayer();

initCarousels();
initAOS();
