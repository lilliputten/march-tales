import { formatDuration, quoteHtmlAttr } from '../helpers/CommonHelpers';

import { localTrackInfoDb } from './localTrackInfoDb';
import { floatingPlayer } from '../entities/FloatingPlayer/floatingPlayer';
import {
  FloatingPlayerFavoriteData,
  FloatingPlayerFavoritesData,
  FloatingPlayerIncrementData,
  FloatingPlayerUpdateData,
} from '../entities/FloatingPlayer/FloatingPlayerCallbacks';
import { floatToStr } from '../helpers/floatToStr';
import { TrackInfo } from './TrackInfo';

let allPlayers: NodeListOf<HTMLElement>;
let currentTrackPlayer: HTMLElement | undefined = undefined;

// Values for dataset statuses
const TRUE = 'true';

function calculateAndUpdateTrackPosition(
  trackNode: HTMLElement,
  position: number,
  _isCurrent?: boolean,
) {
  const timeNode = trackNode.querySelector<HTMLElement>('.time');
  const { dataset } = trackNode;
  const { trackId, trackDuration } = dataset;
  const timeMs = Math.floor(position * 1000);
  const timeFormatted = formatDuration(timeMs);
  const id = Number(trackId);
  const duration = trackDuration ? parseFloat(trackDuration.replace(',', '.')) : 0;
  if (!duration) {
    const error = new Error(`No duration provided for a track: ${id}`);
    // eslint-disable-next-line no-console
    console.error('[tracksPlayer:updateTrackPosition]', error.message, {
      error,
    });
    debugger; // eslint-disable-line no-debugger
  }
  const ratio = position / duration;
  const progress = Math.min(100, ratio * 100);
  requestAnimationFrame(() => {
    dataset.position = floatToStr(position);
    dataset.progress = floatToStr(progress);
    trackNode.style.setProperty('--progress', dataset.progress);
    if (timeNode) {
      timeNode.innerText = timeFormatted;
    }
  });
  localTrackInfoDb.updatePosition(id, position);
  // TODO: Update the floating player if isCurrent?
  return { position, duration, progress };
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
  // const isCurrent = trackNode === currentTrackPlayer;
  const { position = 0, progress = 0, status } = floatingPlayerState;
  const { dataset } = trackNode;
  const timeNode = trackNode.querySelector<HTMLElement>('.time');
  const timeMs = Math.floor(position * 1000);
  const timeFormatted = formatDuration(timeMs);
  requestAnimationFrame(() => {
    if (status) {
      dataset.status = status;
    } else {
      delete dataset.status;
    }
    dataset.position = floatToStr(position);
    dataset.progress = floatToStr(progress);
    trackNode.style.setProperty('--progress', dataset.progress);
    if (timeNode) {
      timeNode.innerText = timeFormatted;
    }
  });
  // calculateAndUpdateTrackPosition(trackNode, position, isCurrent); // Is it required here?
  // TODO: Update the floating player if isCurrent?
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
    const error = new Error('Wrong active track id!');
    // eslint-disable-next-line no-console
    console.error('[tracksPlayer:floatingPlayerPlay]', error.message, {
      id,
      'activePlayerData.id': activePlayerData.id,
      error,
    });
    debugger; // eslint-disable-line no-debugger
    return;
  }
  requestAnimationFrame(() => {
    dataset.status = 'playing';
  });
}

function floatingPlayerStop(data: FloatingPlayerUpdateData) {
  const {
    // floatingPlayerState, // ???
    activePlayerData,
  } = data;
  if (!currentTrackPlayer) {
    throw new Error('No current track player node!');
  }
  const { dataset } = currentTrackPlayer;
  const id = Number(dataset.trackId);
  if (id !== activePlayerData.id) {
    const error = new Error('Wrong active track id!');
    // eslint-disable-next-line no-console
    console.error('[tracksPlayer:floatingPlayerState]', error.message, {
      id,
      'activePlayerData.id': activePlayerData.id,
      error,
    });
    debugger; // eslint-disable-line no-debugger
    return;
  }
  requestAnimationFrame(() => {
    delete dataset.status;
  });
  setTimeout(tryToPlayNextTrack.bind(undefined, currentTrackPlayer), 100);
}

function tryToPlayNextTrack(currentTrackPlayer: HTMLElement) {
  const thisIdx = Array.from(allPlayers).indexOf(currentTrackPlayer);
  const nextIdx = (thisIdx + 1) % allPlayers.length;
  const nextTrackNode = allPlayers[nextIdx];
  if (!nextTrackNode || nextTrackNode === currentTrackPlayer) {
    return;
  }
  playTrackNode(nextTrackNode);
}

function getTrackNode(id: number) {
  const players = Array.from(allPlayers);
  const trackNode = players.find((it) => Number(it.dataset.trackId) === id);
  return trackNode;
}

function stopPreviousPlayer() {
  if (currentTrackPlayer) {
    const { dataset } = currentTrackPlayer;
    requestAnimationFrame(() => {
      currentTrackPlayer!.classList.toggle('current', false);
      delete dataset.status;
      delete dataset.loaded;
      delete dataset.error;
    });
  }
}

function updateTrackPlayedCount(
  trackNode: HTMLElement,
  playedCount?: number,
  _isCurrent?: boolean,
) {
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
    const parent = valueNode.closest('.track-played-count[data-played-count]') as HTMLElement;
    requestAnimationFrame(() => {
      valueNode.innerText = strValue;
      if (parent) {
        parent.dataset.playedCount = strValue;
      }
    });
  }
  // TODO: Update value in the floating player?
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

function playTrackNode(trackNode: HTMLElement) {
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
  requestAnimationFrame(() => {
    allPlayers.forEach((it) => {
      if (it !== trackNode && it.classList.contains('current')) {
        it.classList.toggle('current', false);
      }
    });
    trackNode.classList.toggle('current', true);
  });

  currentTrackPlayer = trackNode;

  const position = parseFloat((dataset.position || '0').replace(',', '.'));
  floatingPlayer.setActiveTrack(trackNode, position);

  floatingPlayer.playCurrentPlayer();

  // Show floating player if has been hidden
  if (!isFloatingPlaying) {
    floatingPlayer.showFloatingPlayer();
  }
}

/** Play button click handler */
function trackPlayHandler(ev: MouseEvent) {
  const controlNode = ev.currentTarget as HTMLElement;
  const trackNode = controlNode.closest('.track-player') as HTMLElement;
  playTrackNode(trackNode);
}

function updateTrackFavoriteInDataset(trackNode: HTMLElement, isFavorite: boolean) {
  const { dataset } = trackNode;
  const { favorite } = dataset;
  const isCurrentFavorite = Boolean(favorite);
  if (isFavorite !== isCurrentFavorite) {
    requestAnimationFrame(() => {
      if (isFavorite) {
        dataset.favorite = TRUE;
      } else {
        delete dataset.favorite;
      }
    });
  }
}

function updateSingleFavoriteCallback({ id, favorite }: FloatingPlayerFavoriteData) {
  const trackNode = getTrackNode(id);
  if (trackNode) {
    updateTrackFavoriteInDataset(trackNode, favorite);
  }
}

function updateFavoritesCallback({ favorites }: FloatingPlayerFavoritesData) {
  allPlayers.forEach((trackNode) => {
    const { dataset } = trackNode;
    const { trackId } = dataset;
    const id = Number(trackId);
    const isFavorite = favorites.includes(id);
    updateTrackFavoriteInDataset(trackNode, isFavorite);
  });
}

function initTrackPlayerNodeControls(trackNode: HTMLElement) {
  const { dataset } = trackNode;
  const { trackId } = dataset;
  const id = Number(trackId || '');
  // Set controls' handlers
  const controls = trackNode.querySelectorAll<HTMLElement>('.track-control');
  controls.forEach((node) => {
    const { dataset } = node;
    const { inited, controlId } = dataset;
    if (inited) {
      return;
    }
    if (controlId === 'toggleFavorite') {
      node.addEventListener('click', () => floatingPlayer.toggleFavoriteById(id));
    }
    if (controlId === 'play') {
      node.addEventListener('click', trackPlayHandler);
    }
    dataset.inited = TRUE;
  });
  dataset.inited = TRUE;
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
  const hasServerData = window.isAuthenticated;
  const isCurrent = activePlayerData?.id == id;
  const trackInfo: TrackInfo | undefined = localTrackInfoDb.getById(id);
  const favorite = hasServerData ? Boolean(dataset.favorite) : !!trackInfo?.favorite;
  if (trackInfo) {
    if (!hasServerData) {
      // If no server data then update favorite from the local db
      if (favorite) {
        updateTrackFavoriteInDataset(trackNode, trackInfo.favorite);
      }
    }
    // TODO: Get position from the server (dataset)
    const {
      duration,
      // position,
      // progress,
    } = calculateAndUpdateTrackPosition(trackNode, trackInfo.position || 0, isCurrent);
    const playedCount = Number(
      trackNode.querySelector<HTMLElement>('.track-played-count')?.dataset.playedCount || '0',
    );
    // Update the local db date...
    if (activePlayerData) {
      activePlayerData.favorite = favorite;
      activePlayerData.duration = duration;
    }
    /* TODO: Update local data (favorite, playedCount) from track node dataset?
     * - id
     * - favorite
     * - lastPlayed
     * - lastUpdated
     * - playedCount
     * - position
     */
    const hasChangedData = playedCount !== trackInfo.playedCount || favorite !== trackInfo.favorite;
    if (hasChangedData) {
      trackInfo.playedCount = playedCount;
      trackInfo.favorite = favorite;
      localTrackInfoDb.save(trackInfo);
    }
  }
  if (isCurrent) {
    activePlayerData.title = dataset.trackTitle || '';
    currentTrackPlayer = trackNode;
    requestAnimationFrame(() => {
      trackNode.classList.toggle('current', true);
    });
    floatingPlayerUpdate({ floatingPlayerState: floatingPlayer.state, activePlayerData });
  }
  initTrackPlayerNodeControls(trackNode);
}

export function initTracksPlayerWrapper(domNode: HTMLElement = document.body) {
  allPlayers = domNode.querySelectorAll<HTMLElement>('.track-player[data-track-media-url]');
  allPlayers.forEach(initTrackPlayerNode);
  floatingPlayer.callbacks.addPlayStartCallback(floatingPlayerPlay);
  floatingPlayer.callbacks.addPlayStopCallback(floatingPlayerStop);
  floatingPlayer.callbacks.addUpdateCallback(floatingPlayerUpdate);
  floatingPlayer.callbacks.addIncrementCallback(updateIncrementCallback);
  floatingPlayer.callbacks.addFavoritesCallback(updateFavoritesCallback);
  floatingPlayer.callbacks.addFavoriteCallback(updateSingleFavoriteCallback);
}
