/**
 * @desc Main entry point module (scripts)
 * @module src/assets/index.ts
 * @changed 2025.01.12, 10:00
 */

import { initTracksPlayerWrapper } from './track-blocks/tracksPlayer';
import { initTrackControlsWrapper } from './track-blocks/trackControls';

initTracksPlayerWrapper();
initTrackControlsWrapper();
