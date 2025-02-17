/**
 * @desc Main entry point module (scripts)
 * @module src/assets/index.ts
 * @changed 2025.02.17, 00:17
 */

import { initTracksPlayerWrapper } from './track-blocks/tracksPlayer';
import { initFloatingPlayer } from './entities/FloatingPlayer/floatingPlayer';

initTracksPlayerWrapper();
initFloatingPlayer();
