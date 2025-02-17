import { formatDuration, quoteHtmlAttr } from '../helpers/CommonHelpers';
import { commonNotify } from '../CommonNotify/CommonNotifySingleton';
import { sendApiRequest } from '../helpers/sendApiRequest';
import { getJsText } from '../helpers/getJsText';

import { localTrackInfoDb } from './localTrackInfoDb';
import { floatingPlayer } from '../entities/FloatingPlayer/floatingPlayer';
import { ActivePlayerData } from '../entities/ActivePlayerData/ActivePlayerData';
import { FloatingPlayerState } from '../entities/FloatingPlayer/FloatingPlayerState';

const sharedPlayerContainer = document.body;

let allPlayers: NodeListOf<HTMLElement>;
let sharedPlayerNode: HTMLElement | undefined = undefined;
let currentTrackPlayer: HTMLElement | undefined = undefined;

interface TSharedPlayerOptions {
  type?: string;
  src?: string;
}

// Values for dataset statuses
const TRUE = 'true';

function ensureSharedPlayer(/* opts: TSharedPlayerOptions = {} */) {
  if (!sharedPlayerNode) {
    sharedPlayerNode = document.createElement('div');
    sharedPlayerNode.classList.add('shared-player');
    const audio = document.createElement('audio');
    audio.addEventListener('loadeddata', sharedPlayerCanPlay);
    sharedPlayerNode.appendChild(audio);
    sharedPlayerContainer.appendChild(sharedPlayerNode);
  }
  return sharedPlayerNode;
}

function ensureSharedPlayerAudio() {
  const sharedPlayer = ensureSharedPlayer();
  const audio = sharedPlayer.getElementsByTagName('audio')[0];
  if (!audio) {
    throw new Error(getJsText('noAudioNodeFound'));
  }
  return audio;
}

function createSharedPlayerSource(opts: TSharedPlayerOptions = {}) {
  // const sharedPlayer = ensureSharedPlayer();
  const audio = ensureSharedPlayerAudio();
  const prevSources = Array.from(audio.getElementsByTagName('source'));
  for (const node of prevSources) {
    node.remove();
  }
  audio.setAttribute('preload', 'auto');
  const source = document.createElement('source');
  source.setAttribute('type', opts.type || 'audio/mpeg');
  if (opts.src) {
    source.setAttribute('src', opts.src);
  }
  // @see https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/loadeddata_event
  audio.addEventListener('canplay', sharedPlayerCanPlay);
  audio.addEventListener('loadeddata', sharedPlayerCanPlay);
  audio.addEventListener('playing', sharedPlayerPlay);
  audio.addEventListener('timeupdate', sharedPlayerTimeUpdate);
  audio.addEventListener('ended', sharedPlayerEnded);
  source.addEventListener('error', sharedPlayerError);
  audio.appendChild(source);
  return source;
}

// REMOVE
function sharedPlayerEnded(_ev: Event) {
  if (!currentTrackPlayer) {
    throw new Error('No current track player node!');
  }
  const dataset = currentTrackPlayer?.dataset;
  if (dataset) {
    delete dataset.status;
  }
  incrementPlayedCount();
}

function updateTrackPosition(trackNode: HTMLElement, position: number, isCurrent?: boolean) {
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
  /* console.log('[tracksPlayer:updateTrackPosition]', {
   *   id,
   *   position,
   *   progress,
   *   ratio,
   *   duration,
   *   timeMs,
   *   timeFormatted,
   *   timeNode,
   *   dataset,
   *   trackNode,
   *   isCurrent,
   * });
   */
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

function updatePlayback(position: number) {
  if (!currentTrackPlayer) {
    return;
  }
  updateTrackPosition(currentTrackPlayer, position, true);
}

function sharedPlayerTimeUpdate(ev: Event) {
  if (!currentTrackPlayer) {
    return;
  }
  const audio = ev.currentTarget as HTMLAudioElement;
  const { currentTime } = audio;
  const dataset = currentTrackPlayer.dataset;
  const loaded = Boolean(dataset.loaded);
  if (loaded) {
    /* // DEBUG
     * const { type, eventPhase } = ev;
     * const position = Number(dataset.position || '');
     * const readyState = audio.readyState;
     * console.log('[tracksPlayer:sharedPlayerTimeUpdate]', {
     *   readyState,
     *   position,
     *   loaded,
     *   currentTime,
     *   audio,
     *   type,
     *   eventPhase,
     *   ev,
     *   dataset,
     * });
     */
    updatePlayback(currentTime);
  }
}

// REMOVE
function sharedPlayerPlay(_ev: Event) {
  if (!currentTrackPlayer) {
    throw new Error('No current track player node!');
  }
  const { dataset } = currentTrackPlayer;
  dataset.status = 'playing';
  // floatingPlayer.showFloatingPlayer(currentTrackPlayer);
}

function floatingPlayerPlay(
  _floatingPlayerState: FloatingPlayerState,
  activePlayerData: ActivePlayerData,
) {
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

function floatingPlayerStop(
  _floatingPlayerState: FloatingPlayerState,
  activePlayerData: ActivePlayerData,
) {
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
  incrementPlayedCount();
}

function getTrackNode(id: number) {
  const players = Array.from(allPlayers);
  const trackNode = players.find((it) => Number(it.dataset.trackId) === id);
  return trackNode;
}

function floatingPlayerUpdate(
  floatingPlayerState: FloatingPlayerState,
  activePlayerData: ActivePlayerData,
) {
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
  console.log('[tracksPlayer:floatingPlayerUpdate]', {
    id,
    status,
    position,
    progress,
    timeMs,
    timeFormatted,
    timeNode,
    dataset,
    currentTrackPlayer,
    isCurrent,
  });
  if (status) {
    dataset.status = status;
  } else {
    delete dataset.status;
  }
  // if (id === 5 && position > 6) {
  //   debugger;
  // }
  dataset.position = String(position);
  dataset.progress = String(progress);
  currentTrackPlayer.style.setProperty('--progress', String(progress));
  if (timeNode) {
    timeNode.innerHTML = timeFormatted;
  }
  localTrackInfoDb.updatePosition(id, position);
  if (isCurrent) {
    // TODO: Update the floating player if isCurrent
  }
}

function updateAudioPosition(trackNode: HTMLElement, isCurrent: boolean = true) {
  const audio = ensureSharedPlayerAudio();
  const dataset = trackNode.dataset;
  const duration = parseFloat((dataset.trackDuration || '0').replace(',', '.'));
  let position = parseFloat((dataset.position || '0').replace(',', '.'));
  /* console.log('[tracksPlayer:updateAudioPosition]', {
   *   readyState: audio.readyState,
   *   currentTime: audio.currentTime,
   *   position,
   *   duration,
   *   dataset,
   *   audio,
   *   // source,
   * });
   */
  if (/* !audio.seekable || */ position >= duration - 0.1) {
    position = 0;
    updateTrackPosition(trackNode, position, isCurrent);
    dataset.position = '0';
    dataset.progress = '0';
    audio.currentTime = 0;
  } else {
    audio.currentTime = position;
  }
}

function audioPlay(trackNode: HTMLElement, isCurrent: boolean = true) {
  const audio = ensureSharedPlayerAudio();
  /* // DEBUG
   * const dataset = trackNode.dataset;
   * dataset.status = 'playing';
   * const duration = parseFloat(dataset.trackDuration.replace(',', '.'));
   * const position = Number(dataset.position || '');
   * console.log('[tracksPlayer:audioPlay]', {
   *   duration,
   *   position,
   *   dataset,
   *   audio,
   *   // source,
   * });
   */
  updateAudioPosition(trackNode, isCurrent);
  audio.play();
}

function sharedPlayerCanPlay(_ev: Event) {
  if (!currentTrackPlayer) {
    throw new Error('No current track player node!');
  }
  const dataset = currentTrackPlayer.dataset;
  const isLoaded = !!dataset.loaded;
  if (!isLoaded) {
    dataset.loaded = TRUE;
    delete dataset.error;
    /* // DEBUG
     * const audio = ensureSharedPlayerAudio();
     * const readyState = audio.readyState;
     * console.log('[tracksPlayer:sharedPlayerCanPlay]', {
     *   readyState,
     *   currentTime: audio.currentTime,
     *   dataset,
     *   audio,
     * });
     */
    // Start playback if all is ok...
    audioPlay(currentTrackPlayer, true);
  }
}

function sharedPlayerError(ev: Event) {
  const srcElement = ev.currentTarget as HTMLSourceElement;
  const { src, type } = srcElement;
  const errMsg = getJsText('errorLoadingAudioFile') + ' ' + src;
  const error = new Error(errMsg);
  // eslint-disable-next-line no-console
  console.error('[sharedPlayerError]', errMsg, {
    error,
    currentTrackPlayer,
    src,
    type,
    ev,
  });
  debugger; // eslint-disable-line no-debugger
  commonNotify.showError(errMsg);
  const dataset = currentTrackPlayer?.dataset;
  if (dataset) {
    dataset.error = errMsg;
    delete dataset.loaded;
    delete dataset.status;
  }
}

function isAudioPlaying(audio: HTMLAudioElement) {
  return !!audio && audio.currentTime > 0 && !audio.paused && !audio.ended && audio.readyState > 2;
}

function stopPreviousPlayer() {
  if (sharedPlayerNode) {
    const audio = sharedPlayerNode.getElementsByTagName('audio')[0];
    if (audio && isAudioPlaying(audio)) {
      audio.pause();
    }
  }
  if (currentTrackPlayer) {
    currentTrackPlayer.classList.toggle('current', false);
    const { dataset } = currentTrackPlayer;
    delete dataset.status;
    delete dataset.loaded;
    delete dataset.error;
  }
}

function sendIncrementPlayedCount() {
  const { dataset } = currentTrackPlayer;
  const { trackId } = dataset;
  const url = `/api/v1/tracks/${trackId}/increment-played-count/`;
  return sendApiRequest(url, 'POST');
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

function incrementPlayedCount() {
  if (!currentTrackPlayer) {
    throw new Error('No current track player node!');
  }
  const trackNode = currentTrackPlayer;
  const { dataset } = trackNode;
  if (dataset.incrementing) {
    return;
  }
  dataset.incrementing = TRUE;
  updateTrackPlayedCount(trackNode, undefined, true);
  if (!window.isAuthenticated) {
    delete dataset.incrementing;
    return;
  }
  return sendIncrementPlayedCount()
    .then(({ played_count }: { played_count?: number }) => {
      if (played_count != null) {
        // Re-update local data with server data...
        updateTrackPlayedCount(trackNode, played_count, true);
      }
      // TODO: Update other instances of this track on the page (eg, in player, or in other track listings)?
    })
    .catch((err) => {
      // eslint-disable-next-line no-console
      console.error('[tracksPlayer:incrementPlayedCount:sendIncrementPlayedCount] error', {
        err,
      });
      debugger; // eslint-disable-line no-debugger
      commonNotify.showError(err);
      throw err;
    })
    .finally(() => {
      delete dataset.incrementing;
    });
}

function startPlay() {
  if (!currentTrackPlayer) {
    throw new Error('No current track player node!');
  }
  const { dataset } = currentTrackPlayer;
  const isLoaded = !!dataset.loaded;
  const audio = ensureSharedPlayerAudio();
  if (!isLoaded) {
    dataset.status = 'waiting';
    delete dataset.loaded;
    delete dataset.error;
    const { trackMediaUrl } = dataset;
    const source = createSharedPlayerSource({ src: trackMediaUrl });
    if (!source) {
      throw new Error(getJsText('noAudioSourceNodeFound'));
    }
    updateAudioPosition(currentTrackPlayer, true);
    // see `sharedPlayerLoaded`, `sharedPlayerCanPlay` handlers
    audio.load();
  } else {
    audioPlay(currentTrackPlayer, true);
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
    floatingPlayerUpdate(floatingPlayer.state, activePlayerData);
  } else if (trackInfo) {
    const position = trackInfo.position;
    if (position) {
      updateTrackPosition(trackNode, position, false);
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
}
