/**
 * @desc Main entry point module (scripts)
 * @module src/assets/index.ts
 * @changed 2025.02.13, 04:41
 */

import { initTracksPlayerWrapper } from './track-blocks/tracksPlayer';
import { initFloatingPlayer } from './track-blocks/floatingPlayer';

initTracksPlayerWrapper();
initFloatingPlayer();
