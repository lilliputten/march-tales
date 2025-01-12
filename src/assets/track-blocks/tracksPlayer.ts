import { formatDuration } from '../helpers/CommonHelpers';
import { commonNotify } from '../CommonNotify/CommonNotifySingleton';

const sharedPlayerContainer = document.body;

let sharedPlayerNode: HTMLElement | undefined = undefined;
let currentTrackPlayer: HTMLElement | undefined = undefined;

interface TSharedPlayerOptions {
  type?: string;
  src?: string;
}

// Values for dataset ststuses
const TRUE = 'true';
// const FALSE = ''; // NOTE: Using `delete` operator

function ensureSharedPlayer(/* opts: TSharedPlayerOptions = {} */) {
  if (!sharedPlayerNode) {
    sharedPlayerNode = document.createElement('div');
    sharedPlayerNode.classList.add('shared-player');
    const audio = document.createElement('audio');
    audio.addEventListener('loadeddata', sharedPlayerLoaded);
    sharedPlayerNode.appendChild(audio);
    sharedPlayerContainer.appendChild(sharedPlayerNode);
  }
  return sharedPlayerNode;
}

function ensureSharedPlayerAudio() {
  const sharedPlayer = ensureSharedPlayer();
  const audio = sharedPlayer.getElementsByTagName('audio')[0];
  if (!audio) {
    throw new Error('No audio node found');
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
  audio.addEventListener('loadeddata', sharedPlayerLoaded);
  audio.addEventListener('playing', sharedPlayerPlay);
  audio.addEventListener('timeupdate', sharedPlayerTimeUpdate);
  audio.addEventListener('ended', sharedPlayerEnded);
  source.addEventListener('error', sharedPlayerError);
  audio.appendChild(source);
  return source;
}

function sharedPlayerEnded(_ev: Event) {
  const audio = ensureSharedPlayerAudio();
  /* console.log('[sharedPlayerEnded]', {
   *   ev,
   * });
   */
  // Rewind for the next play
  audio.currentTime = 0;
  // Update status
  const dataset = currentTrackPlayer?.dataset;
  if (dataset) {
    delete dataset.status;
  }
}

function sharedPlayerTimeUpdate(ev: Event) {
  const timeNode = currentTrackPlayer?.querySelector('.time');
  const audio = ev.currentTarget as HTMLAudioElement;
  const { currentTime } = audio;
  if (timeNode) {
    const secs = Math.floor(currentTime * 1000);
    const durationFormatted = formatDuration(secs);
    timeNode.innerHTML = durationFormatted;
  }
  /* console.log('[sharedPlayerTimeUpdate]', {
   *   timeNode,
   *   currentTime,
   *   ev,
   * });
   */
  const dataset = currentTrackPlayer?.dataset;
  if (dataset) {
    // dataset.status = 'playing';
  }
}

function sharedPlayerPlay(_ev: Event) {
  /* console.log('[sharedPlayerPlay]', {
   *   ev,
   * });
   */
  const dataset = currentTrackPlayer?.dataset;
  if (dataset) {
    dataset.status = 'playing';
  }
}

function sharedPlayerLoaded(_ev: Event) {
  const audio = ensureSharedPlayerAudio();
  /* console.log('[sharedPlayerLoaded]', {
   *   ev,
   * });
   */
  const dataset = currentTrackPlayer?.dataset;
  if (dataset) {
    dataset.loaded = TRUE;
    delete dataset.error;
  }
  audio.play();
}

function sharedPlayerError(ev: Event) {
  const srcElement = ev.currentTarget as HTMLSourceElement;
  const { src, type } = srcElement;
  const errMsg = 'Error loading audio file ' + src;
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
  // TODO: Show toast
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
      audio.currentTime = 0;
    }
  }
  if (currentTrackPlayer) {
    const { dataset } = currentTrackPlayer;
    delete dataset.status;
    delete dataset.loaded;
    delete dataset.error;
  }
}

function trackPlayHandler(ev: MouseEvent) {
  const controlNode = ev.currentTarget as HTMLElement;
  const trackControlsNode = controlNode.closest('.track-controls') as HTMLElement;
  const trackPlayer = controlNode.closest('.track-player') as HTMLElement;
  if (currentTrackPlayer && currentTrackPlayer !== trackPlayer) {
    stopPreviousPlayer();
  }
  const { dataset } = trackPlayer;
  const isPlaying = dataset.status === 'playing';
  const isWaiting = dataset.status === 'waiting';
  const isLoaded = !!dataset.loaded;
  const readyToPlay = !isWaiting && !isPlaying;
  const audio = ensureSharedPlayerAudio();
  /* console.log('[tracksPlayer:trackPlayHandler]', {
   *   // isError,
   *   isPlaying,
   *   isWaiting,
   *   isLoaded,
   *   // isPaused,
   *   readyToPlay,
   *   controlNode,
   *   trackControlsNode,
   *   trackPlayer,
   * });
   */
  if (isPlaying) {
    // Pause if playing...
    audio.pause();
    dataset.status = 'paused';
  } else if (readyToPlay) {
    // Play if hasn't played now...
    currentTrackPlayer = trackPlayer;
    if (!isLoaded) {
      dataset.status = 'waiting';
      delete dataset.loaded;
      delete dataset.error;
      const { trackMediaUrl } = dataset;
      const source = createSharedPlayerSource({ src: trackMediaUrl });
      if (!source) {
        throw new Error('No audio source node found');
      }
      audio.load();
    } else {
      dataset.status = 'playing';
      audio.play();
    }
  }
}

function initTrackPlayerNode(playerNode: HTMLElement) {
  const { dataset } = playerNode;
  const {
    inited,
    // trackId, // "1"
    trackMediaUrl, // "/media/samples/gr-400x225.jpg"
  } = dataset;
  if (inited || !trackMediaUrl) {
    return;
  }
  const playControl = playerNode.querySelector('.track-controls .track-control-play');
  playControl.addEventListener('click', trackPlayHandler);
  dataset.inited = TRUE;
}

export function initTracksPlayerWrapper(domNode: HTMLElement = document.body) {
  const players = domNode.querySelectorAll('.track-player[data-track-media-url]');
  players.forEach(initTrackPlayerNode);
}
