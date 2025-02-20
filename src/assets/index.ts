/**
 * @desc Main entry point module (scripts)
 * @module src/assets/index.ts
 * @changed 2025.02.17, 00:17
 */

import { checkProjectVersion } from './checkProjectVersion';
import { initTracksPlayerWrapper } from './track-blocks/tracksPlayer';
import { initFloatingPlayer } from './entities/FloatingPlayer/floatingPlayer';
import { processTextContent } from './processTextContent';

checkProjectVersion();
processTextContent();

initTracksPlayerWrapper();
initFloatingPlayer();
