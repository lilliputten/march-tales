import { formatDuration, quoteHtmlAttr } from '../helpers/CommonHelpers';
import { commonNotify } from '../CommonNotify/CommonNotifySingleton';
import { sendApiRequest } from '../helpers/sendApiRequest';
import { getJsText } from '../helpers/getJsText';

import { localTrackInfoDb } from './localTrackInfoDb';
import { floatingPlayer } from '../entities/FloatingPlayer/floatingPlayer';
import {
  FloatingPlayerIncrementData,
  FloatingPlayerUpdateData,
} from '../entities/FloatingPlayer/FloatingPlayerCallbacks';

// const sharedPlayerContainer = document.body;

let allPlayers: NodeListOf<HTMLElement>;
// let sharedPlayerNode: HTMLElement | undefined = undefined;
let currentTrackPlayer: HTMLElement | undefined = undefined;

// Values for dataset statuses
const TRUE = 'true';

function calculateAndUpdateTrackPosition(
  trackNode: HTMLElement,
  position: number,
  isCurrent?: boolean,
) {
  const timeNode = trackNode.querySelector('.time');
  const { dataset } = trackNode;
  const { trackId, trackDuration } = dataset;
  const timeMs = Math.floor(position * 1000);
  const timeFormatted = formatDuration(timeMs);
  const id = Number(trackId);
  const duration = parseFloat(trackDuration.replace(',', '.'));
  if (!duration) {
    const error = new Error(`No duration provided for a track: ${id}`);
    // eslint-disable-next-line no-console
    console.error('[tracksPlayer:updateTrackPosition]', error.message, {
      error,
    });
    debugger; // eslint-disable-line no-debugger
  }
  const ratio = position / duration;
  const progress = Math.round(ratio * 100);
  dataset.position = String(position);
  dataset.progress = String(progress);
  trackNode.style.setProperty('--progress', String(progress));
  if (timeNode) {
    timeNode.innerHTML = timeFormatted;
  }
  localTrackInfoDb.updatePosition(id, position);
  if (isCurrent) {
    // TODO: Update the floating player if isCurrent
  }
}

function floatingPlayerUpdate(data: FloatingPlayerUpdateData) {
  const { floatingPlayerState, activePlayerData } = data;
  const { id } = activePlayerData;
  let trackNode = currentTrackPlayer;
  if (!trackNode || Number(trackNode.dataset.trackId) !== id) {
    trackNode = getTrackNode(id);
  }
  if (!trackNode) {
    return;
  }
  const isCurrent = trackNode === currentTrackPlayer;
  const { position, progress, status } = floatingPlayerState;
  const { dataset } = currentTrackPlayer;
  const timeNode = currentTrackPlayer.querySelector('.time');
  const timeMs = Math.floor(position * 1000);
  const timeFormatted = formatDuration(timeMs);
  if (status) {
    dataset.status = status;
  } else {
    delete dataset.status;
  }
  dataset.position = String(position);
  dataset.progress = String(progress);
  calculateAndUpdateTrackPosition(trackNode, position, isCurrent);
  currentTrackPlayer.style.setProperty('--progress', String(progress));
  if (timeNode) {
    timeNode.innerHTML = timeFormatted;
  }
  if (isCurrent) {
    // TODO: Update the floating player if isCurrent
  }
}

function floatingPlayerPlay(data: FloatingPlayerUpdateData) {
  const {
    // floatingPlayerState,
    activePlayerData,
  } = data;
  if (!currentTrackPlayer) {
    throw new Error('No current track player node!');
  }
  const { dataset } = currentTrackPlayer;
  const id = Number(dataset.trackId);
  if (id !== activePlayerData.id) {
    throw new Error('Wrong active track id!');
  }
  dataset.status = 'playing';
  // floatingPlayer.showFloatingPlayer(currentTrackPlayer);
}

function floatingPlayerStop(data: FloatingPlayerUpdateData) {
  const {
    // floatingPlayerState,
    activePlayerData,
  } = data;
  if (!currentTrackPlayer) {
    throw new Error('No current track player node!');
  }
  const { dataset } = currentTrackPlayer;
  const id = Number(dataset.trackId);
  if (id !== activePlayerData.id) {
    throw new Error('Wrong active track id!');
  }
  if (dataset) {
    delete dataset.status;
  }
  // incrementPlayedCount();
}

function getTrackNode(id: number) {
  const players = Array.from(allPlayers);
  const trackNode = players.find((it) => Number(it.dataset.trackId) === id);
  return trackNode;
}

function stopPreviousPlayer() {
  if (currentTrackPlayer) {
    currentTrackPlayer.classList.toggle('current', false);
    const { dataset } = currentTrackPlayer;
    delete dataset.status;
    delete dataset.loaded;
    delete dataset.error;
  }
}

function updateTrackPlayedCount(trackNode: HTMLElement, playedCount?: number, isCurrent?: boolean) {
  const { dataset } = trackNode;
  const { trackId } = dataset;
  const id = Number(trackId);
  if (!id) {
    throw new Error('No current track id!');
  }
  const updatedTrackInfo = localTrackInfoDb.updatePlayedCount(id, playedCount);
  const { playedCount: updatedPlayedCount } = updatedTrackInfo;
  const strValue = quoteHtmlAttr(String(updatedPlayedCount));
  const valueNode = trackNode.querySelector('#played_count') as HTMLElement;
  // Update counter in the document...
  if (valueNode) {
    valueNode.innerText = strValue;
    // ???
    const parent = valueNode.closest('.track-played-count[data-played-count]') as HTMLElement;
    if (parent) {
      parent.dataset.playedCount = strValue;
    }
  }
  if (isCurrent) {
    // TODO: Update value in the floating player
  }
}

function updateIncrementCallback(data: FloatingPlayerIncrementData) {
  const {
    count,
    // floatingPlayerState,
    activePlayerData,
  } = data;
  const trackNode = getTrackNode(activePlayerData.id);
  const isCurrent = trackNode === currentTrackPlayer;
  if (trackNode) {
    updateTrackPlayedCount(trackNode, count, isCurrent);
  }
}

/** Play button click handler */
function trackPlayHandler(ev: MouseEvent) {
  const controlNode = ev.currentTarget as HTMLElement;
  const trackNode = controlNode.closest('.track-player') as HTMLElement;
  // Reset previous player
  if (currentTrackPlayer && currentTrackPlayer !== trackNode) {
    stopPreviousPlayer();
  }
  const { dataset } = trackNode;
  const id = Number(dataset.trackId);

  const playingId = floatingPlayer.getActiveTrackId();
  const isFloatingPlaying = floatingPlayer.isPlaying();
  if (isFloatingPlaying) {
    // Pause playback
    floatingPlayer.pauseCurrentPlayer();
    if (playingId === id) {
      // Return -- just pause current track
      return;
    }
  }

  // Clear all tracks active status?
  trackNode.classList.toggle('current', true);
  currentTrackPlayer = trackNode;

  const position = parseFloat((dataset.position || '0').replace(',', '.'));
  floatingPlayer.setActiveTrack(trackNode, position);

  floatingPlayer.playCurrentPlayer();

  // Show floating player if has been hidden
  if (!isFloatingPlaying) {
    floatingPlayer.showFloatingPlayer();
  }
}

function sendToggleFavoriteRequest(trackId: number | string, value: boolean) {
  const url = `/api/v1/tracks/${trackId}/toggle-favorite/`;
  return sendApiRequest(url, 'POST', { value });
}

function updateTrackFavorite(trackNode: HTMLElement, isFavorite: boolean) {
  const { dataset } = trackNode;
  const { favorite } = dataset;
  const isCurrentFavorite = Boolean(favorite);
  if (isFavorite !== isCurrentFavorite) {
    if (isFavorite) {
      dataset.favorite = TRUE;
    } else {
      delete dataset.favorite;
    }
  }
}

function updateFavoritesByTrackIds(ids: number[]) {
  localTrackInfoDb.updateFavoritesByTrackIds(ids);
  allPlayers.forEach((trackNode) => {
    const { dataset } = trackNode;
    const { trackId } = dataset;
    const id = Number(trackId);
    const isFavorite = ids.includes(id);
    updateTrackFavorite(trackNode, isFavorite);
  });
}

function toggleFavorite(ev: Event) {
  const node = ev.currentTarget as HTMLElement;
  const trackNode = node.closest<HTMLElement>('.track-player');
  const { dataset } = trackNode;
  const { trackId, favorite } = dataset;
  const id = Number(trackId);
  if (!id) {
    throw new Error('No current track id!');
  }
  const nextFavorite = !favorite;
  localTrackInfoDb.updateFavorite(id, nextFavorite);
  if (nextFavorite) {
    dataset.favorite = TRUE;
  } else {
    delete dataset.favorite;
  }
  if (window.isAuthenticated) {
    sendToggleFavoriteRequest(trackId, nextFavorite)
      .then((results: { favorite_track_ids: number[] }) => {
        const { favorite_track_ids } = results;
        /* console.log('[trackControls:toggleFavorite]', {
         *   favorite_track_ids,
         * });
         */
        updateFavoritesByTrackIds(favorite_track_ids);
        const msgId = nextFavorite ? 'trackAddedToFavorites' : 'trackRemovedFromFavorites';
        commonNotify.showSuccess(getJsText(msgId));
      })
      .catch((err) => {
        // eslint-disable-next-line no-console
        console.error('[tracksPlayer:toggleFavorite:sendToggleFavoriteRequest] error', {
          err,
        });
        debugger; // eslint-disable-line no-debugger
        commonNotify.showError(err);
      });
  }
}

function initTrackPlayerNode(trackNode: HTMLElement) {
  const activePlayerData = floatingPlayer.activePlayerData;
  const { dataset } = trackNode;
  const {
    inited,
    trackId, // "1"
    trackMediaUrl, // "/media/samples/gr-400x225.jpg"
  } = dataset;
  const id = Number(trackId || '');
  if (!id || inited || !trackMediaUrl) {
    return;
  }
  const trackInfo = localTrackInfoDb.getById(id);
  if (activePlayerData && activePlayerData.id == id) {
    currentTrackPlayer = trackNode;
    trackNode.classList.toggle('current', true);
    // dataset.status = floatingPlayer.state.status;
    floatingPlayerUpdate({ floatingPlayerState: floatingPlayer.state, activePlayerData });
  } else if (trackInfo) {
    const position = trackInfo.position;
    if (position) {
      calculateAndUpdateTrackPosition(trackNode, position, false);
    }
  }
  if (trackInfo) {
    if (!window.isAuthenticated) {
      if (trackInfo?.favorite) {
        updateTrackFavorite(trackNode, trackInfo.favorite);
      }
    }
  }
  const controls = trackNode.querySelectorAll<HTMLElement>('.track-control');
  controls.forEach((node) => {
    const { dataset } = node;
    const { inited, controlId } = dataset;
    if (inited) {
      return;
    }
    if (controlId === 'toggleFavorite') {
      node.addEventListener('click', toggleFavorite);
    }
    if (controlId === 'play') {
      node.addEventListener('click', trackPlayHandler);
    }
    dataset.inited = TRUE;
  });
  dataset.inited = TRUE;
}

export function initTracksPlayerWrapper(domNode: HTMLElement = document.body) {
  allPlayers = domNode.querySelectorAll<HTMLElement>('.track-player[data-track-media-url]');
  allPlayers.forEach(initTrackPlayerNode);
  floatingPlayer.callbacks.addPlayStartCallback(floatingPlayerPlay);
  floatingPlayer.callbacks.addPlayStopCallback(floatingPlayerStop);
  floatingPlayer.callbacks.addUpdateCallback(floatingPlayerUpdate);
  floatingPlayer.callbacks.addIncrementCallback(updateIncrementCallback);
  // TODO: Add toggle favorite callback
}
