import { getJsText } from '../../helpers/getJsText';
import { commonNotify } from '../../CommonNotify/CommonNotifySingleton';
import { formatDuration, getErrorText } from '../../helpers/CommonHelpers';
import { localTrackInfoDb } from '../../track-blocks/localTrackInfoDb';

import {
  ActivePlayerData,
  loadActivePlayerData,
  saveActivePlayerData,
} from '../ActivePlayerData/ActivePlayerData';
import { getActivePlayerDataFromTrackNode } from '../ActivePlayerData/getActivePlayerDataFromTrackNode';
import { sendApiRequest } from '../../helpers/sendApiRequest';
import { floatToStr } from '../../helpers/floatToStr';
import {
  FloatingPlayerState,
  loadFloatingPlayerState,
  saveFloatingPlayerState,
} from './FloatingPlayerState';

import { HiddenPlayer } from './HiddenPlayer';
import { FloatingPlayerCallbacks } from './FloatingPlayerCallbacks';

// TODO: Update track title on the language change?

const TRUE = 'true';

/** A value of forward/backward seek step */
const seekTimeSec = 1;

export class FloatingPlayer {
  inited = false;
  callbacks = new FloatingPlayerCallbacks();
  audio?: HTMLAudioElement;
  hiddenPlayer: HiddenPlayer = new HiddenPlayer();
  activePlayerData?: ActivePlayerData;
  state: FloatingPlayerState = {};
  domNode?: HTMLElement;
  incrementing?: boolean;
  toggling: Record<number, boolean> = {};
  seeking = false;

  constructor() {
    this.loadActivePlayerData();
    this.loadFloatingPlayerState();
    this.initDomNode();
    this.updateAll();
    // Check if it was recently playing...
    const now = Date.now();
    if (this.activePlayerData) {
      this.ensureAudioLoaded();
      if (
        this.state.status === 'playing' &&
        this.state.lastTimestamp &&
        this.state.lastTimestamp > now - 5000
      ) {
        // TODO: Then resume playback...
        /* console.log('[FloatingPlayerClass:constructor] Start play', {
         *   activePlayerData: this.activePlayerData,
         *   state: this.state,
         * });
         */
        // TODO: Care about: `Uncaught (in promise) NotAllowedError: play() failed because the user didn't interact with the document first. https://goo.gl/xX8pDD`
        this.playCurrentPlayer();
      } else {
        // Reset the status
        delete this.state.status;
      }
    }
  }

  requireAudio() {
    if (!this.audio) {
      this.audio = this.hiddenPlayer.ensureHiddenPlayerAudio();
      this.audio.addEventListener('canplay', this.handleAudioCanPlay.bind(this));
      this.audio.addEventListener('playing', this.handleAudioPlay.bind(this));
      this.audio.addEventListener('timeupdate', this.handleAudioTimeUpdate.bind(this));
      this.audio.addEventListener('ended', this.handleAudioEnded.bind(this));
      // source.addEventListener('error', this.handleAudioSourceError.bind(this));
    }
    return this.audio;
  }

  removeAudio() {
    this.hiddenPlayer.removeHiddenPlayerAudio();
    this.audio = undefined;
  }

  hasAudio() {
    return !!this.audio;
  }

  hasAudioSource() {
    return this.hiddenPlayer.hasSource();
  }

  requireDomNode() {
    if (!this.domNode) {
      this.domNode = document.querySelector<HTMLElement>('.floating-player');
      this.hiddenPlayer.setParentDomNode(this.domNode);
    }
    // TODO: Ensure created dom node?
    if (!this.domNode) {
      const error = new Error('No floating player node found');
      // eslint-disable-next-line no-console
      console.error('[FloatingPlayerClass:requireDomNode]', error.message, {
        error,
      });
      debugger; // eslint-disable-line no-debugger
      throw error;
    }
    return this.domNode;
  }

  requireActivePlayerData() {
    // TODO: Ensure data?
    if (!this.activePlayerData) {
      const error = new Error('No active player data set');
      // eslint-disable-next-line no-console
      console.error('[FloatingPlayerClass:requireActivePlayerData]', error.message, {
        error,
      });
      debugger; // eslint-disable-line no-debugger
      throw error;
    }
    return this.activePlayerData;
  }

  // Sync persistent data...

  loadActivePlayerData() {
    this.activePlayerData = loadActivePlayerData();
  }

  saveActivePlayerData() {
    saveActivePlayerData(this.activePlayerData);
  }

  loadFloatingPlayerState() {
    this.state = loadFloatingPlayerState();
  }

  saveFloatingPlayerState() {
    saveFloatingPlayerState(this.state);
  }

  // Dom node...

  showFloatingPlayer() {
    this.state.visible = true;
    this.updateStateInDom();
    this.saveFloatingPlayerState();
  }

  hideFloatingPlayer() {
    this.state.visible = false;
    this.updateStateInDom();
    this.saveFloatingPlayerState();
  }

  // Updaters...

  updateActivePlayerDataInDom() {
    const domNode = this.requireDomNode();
    const activePlayerData = this.requireActivePlayerData();
    const id = activePlayerData.id;
    const titleNode = domNode.querySelector<HTMLElement>('.title');
    const durationNode = domNode.querySelector<HTMLElement>('.duration');
    const imageNode = domNode.querySelector<HTMLElement>('.image');
    const { dataset } = domNode;
    requestAnimationFrame(() => {
      titleNode.innerText = activePlayerData.title;
      durationNode.innerText = formatDuration(Math.floor(activePlayerData.duration * 1000));
      imageNode.style.backgroundImage = 'url(' + activePlayerData.imageUrl + ')';
      if (activePlayerData.favorite) {
        dataset.favorite = TRUE;
      } else {
        delete dataset.favorite;
      }
      const links = domNode.querySelectorAll<HTMLLinkElement>('.trackLink');
      links.forEach((it) => {
        it.setAttribute('href', `/tracks/${id}`);
      });
    });
  }

  updateStateInDom() {
    const domNode = this.requireDomNode();
    const { dataset } = domNode;
    requestAnimationFrame(() => {
      if (this.state.status) {
        dataset.status = this.state.status;
      } else {
        delete dataset.status;
      }
      document.body.classList.toggle('withPlayer', !!this.state.visible);
    });
  }

  updatePositionInDom() {
    const domNode = this.requireDomNode();
    const seekBarNode = domNode.querySelector<HTMLInputElement>('.seekBar');
    const { dataset } = domNode;
    requestAnimationFrame(() => {
      dataset.position = floatToStr(this.state.position);
      dataset.progress = floatToStr(this.state.progress);
      domNode.style.setProperty('--progress', dataset.progress);
      seekBarNode.value = dataset.progress;
    });
  }

  calculateProgress() {
    const activePlayerData = this.requireActivePlayerData();
    const { position } = this.state;
    const { id, duration } = activePlayerData;
    if (!duration) {
      const error = new Error(`No duration provided for a track: ${id}`);
      // eslint-disable-next-line no-console
      console.error('[FloatingPlayerClass:calculateProgress]', error.message, {
        error,
      });
      debugger; // eslint-disable-line no-debugger
      throw error;
    }
    const ratio = position / duration;
    const progress = Math.min(100, ratio * 100);
    return progress;
  }

  updateTrackPosition() {
    const domNode = this.requireDomNode();
    const timeNode = domNode.querySelector<HTMLElement>('.time');
    const activePlayerData = this.requireActivePlayerData();
    const { position } = this.state;
    const { id } = activePlayerData;
    const progress = this.calculateProgress();
    this.state.progress = progress;
    this.updatePositionInDom();
    if (timeNode) {
      requestAnimationFrame(() => {
        timeNode.innerText = formatDuration(Math.floor(position * 1000));
      });
    }
    localTrackInfoDb.updatePosition(id, position);
  }

  updateAll() {
    if (this.activePlayerData) {
      this.updateTrackPosition();
    }
    this.updateStateInDom();
    this.updatePositionInDom();
    if (this.activePlayerData) {
      this.updateActivePlayerDataInDom();
    }
  }

  // Audio handlers...

  handleAudioTimeUpdate(ev: Event) {
    if (this.seeking) {
      return;
    }
    const currAudio = this.audio;
    const audio = ev.currentTarget as HTMLAudioElement;
    if (audio !== currAudio) {
      return;
    }
    const activePlayerData = this.requireActivePlayerData();
    const {
      currentTime,
      // readyState, // DEBUG
    } = audio;
    /* // DEBUG
     * const source = audio.getElementsByTagName('SOURCE')[0] as HTMLSourceElement;
     * console.log('[FloatingPlayerClass:handleAudioTimeUpdate]', {
     *   currentTime,
     *   readyState,
     *   id: activePlayerData.id,
     *   activePlayerData,
     *   src: source.src,
     *   source,
     *   thisAudio: currAudio === audio,
     *   currAudio,
     *   audio,
     * });
     */
    // TODO: Check loaded status?
    if (this.state.position != currentTime) {
      this.state.position = currentTime;
      this.updateTrackPosition();
      this.saveFloatingPlayerState();
      this.callbacks.invokeUpdate({ floatingPlayerState: this.state, activePlayerData });
      localTrackInfoDb.updatePosition(activePlayerData.id, currentTime);
    }
  }

  handleAudioCanPlay(_ev: Event) {
    if (!this.state.loaded) {
      this.state.loaded = true;
      delete this.state.error;
    }
  }

  handleAudioPlay(_ev: Event) {
    this.state.status = 'playing';
    this.updateStateInDom();
    this.saveFloatingPlayerState();
    this.callbacks.invokePlayStart({
      floatingPlayerState: this.state,
      activePlayerData: this.activePlayerData,
    });
  }

  handleAudioEnded(_ev: Event) {
    this.incrementPlayedCount();
    this.state.status = 'paused'; // stopped, ready?
    this.updateStateInDom();
    this.saveFloatingPlayerState();
    this.callbacks.invokePlayStop({
      floatingPlayerState: this.state,
      activePlayerData: this.activePlayerData,
    });
  }

  handleError(err: Error | string) {
    const errName = err instanceof Error && err.name;
    // eslint-disable-next-line no-console
    console.error('[FloatingPlayerClass:handleError]', {
      err,
    });
    if (errName === 'AbortError') {
      // NOTE: Do nothing on abort
      return;
    }
    debugger; // eslint-disable-line no-debugger
    this.state.error = getErrorText(err);
    this.updateStateInDom();
    commonNotify.showError(err);
    this.callbacks.invokeError(err);
  }

  handleAudioSourceError(ev: Event) {
    const srcElement = ev.currentTarget as HTMLSourceElement;
    const { src, type } = srcElement;
    const errMsg = getJsText('errorLoadingAudioFile') + ' ' + src + (type ? `( ${type})` : '');
    const error = new Error(errMsg);
    this.handleError(error);
  }

  /// Active player data

  getActiveTrackId(): number | undefined {
    return this.activePlayerData ? this.activePlayerData.id : undefined;
  }

  // Core handlers...

  loadAudio() {
    const activePlayerData = this.requireActivePlayerData();
    this.state.loaded = false;
    const source = this.hiddenPlayer.createHiddenPlayerSource({ src: activePlayerData.mediaUrl });
    source.addEventListener('error', this.handleAudioSourceError.bind(this));
  }

  isAudioPlaying() {
    const audio = this.audio;
    return (
      !!audio && audio.currentTime > 0 && !audio.paused && !audio.ended && audio.readyState > 2
    );
  }

  isPlaying() {
    return this.state.status === 'playing';
  }

  pauseCurrentPlayer() {
    if (this.isAudioPlaying()) {
      const audio = this.requireAudio();
      audio.pause();
    }
    if (this.isPlaying()) {
      this.state.status = 'paused';
      this.updateStateInDom();
      this.saveFloatingPlayerState();
    }
  }

  playCurrentPlayer() {
    const audio = this.requireAudio();
    const activePlayerData = this.requireActivePlayerData();
    if (this.isAudioPlaying()) {
      return;
    }
    if (audio.ended || this.state.position > activePlayerData.duration - 0.1) {
      // Start from the begining
      this.state.position = 0;
      audio.load();
    }
    this.updateTrackPosition();
    this.callbacks.invokeUpdate({
      floatingPlayerState: this.state,
      activePlayerData: this.activePlayerData,
    });

    audio.currentTime = this.state.position || 0;
    const result = audio.play();
    result.catch((err) => {
      if (err.name === 'NotAllowedError') {
        //  play() failed because the user didn't interact with the document first. -> Just cancel
        this.state.status = undefined;
        this.updateStateInDom();
      } else {
        this.handleError(err);
      }
    });
  }

  /** Play button click handler */
  trackPlayHandler(_ev: MouseEvent) {
    const isPlaying = this.isPlaying();
    if (isPlaying) {
      this.pauseCurrentPlayer();
    } else {
      this.playCurrentPlayer();
    }
  }

  // Active player track data...

  ensureAudioLoaded() {
    if (!this.state.loaded || !this.hasAudio() || !this.hasAudioSource) {
      this.loadAudio();
    }
  }

  setActivePlayerData(activePlayerData: ActivePlayerData, position?: number) {
    if (this.activePlayerData?.id !== activePlayerData.id) {
      if (this.activePlayerData && this.isPlaying) {
        this.pauseCurrentPlayer();
      }
      this.state.loaded = false;
      if (position != null) {
        this.state.position = position;
      }
      this.removeAudio();
      this.activePlayerData = activePlayerData;
    }
    this.saveActivePlayerData();
    this.updateActivePlayerDataInDom();
    this.ensureAudioLoaded();
  }

  setActiveTrack(trackNode: HTMLElement, position?: number) {
    const activePlayerData = getActivePlayerDataFromTrackNode(trackNode);
    this.setActivePlayerData(activePlayerData, position);
  }

  clearActiveData() {
    this.activePlayerData = undefined;
    this.hideFloatingPlayer();
    this.removeAudio();
  }

  // Update related data

  sendIncrementPlayedCount(id: number) {
    const url = `/api/v1/tracks/${id}/increment-played-count/`;
    return sendApiRequest(url, 'POST');
  }

  incrementPlayedCount() {
    const activePlayerData = this.requireActivePlayerData();
    if (this.incrementing) {
      return;
    }
    this.incrementing = true;
    return this.sendIncrementPlayedCount(activePlayerData.id)
      .then(({ played_count }: { played_count?: number }) => {
        if (played_count != null) {
          // Re-update local data with server data...
          this.callbacks.invokeIncrement({ count: played_count, activePlayerData });
        }
        // TODO: Update other instances of this track on the page (eg, in player, or in other track listings)?
      })
      .catch((err) => {
        // eslint-disable-next-line no-console
        console.error('[FloatingPlayerClass:incrementPlayedCount:sendIncrementPlayedCount] error', {
          err,
        });
        debugger; // eslint-disable-line no-debugger
        commonNotify.showError(err);
        // Increment locally (?)
        this.callbacks.invokeIncrement({ activePlayerData });
        throw err;
      })
      .finally(() => {
        this.incrementing = false;
      });
  }

  sendToggleFavoriteRequest(id: number, value: boolean) {
    const url = `/api/v1/tracks/${id}/toggle-favorite/`;
    return sendApiRequest(url, 'POST', { value });
  }

  toggleFavorite() {
    const activePlayerData = this.requireActivePlayerData();
    const id = activePlayerData.id;
    this.toggleFavoriteById(id);
  }

  toggleFavoriteById(id: number) {
    if (this.toggling[id]) {
      return;
    }
    const activePlayerData = this.activePlayerData;
    const isCurrent = id === activePlayerData?.id;
    const trackInfo = localTrackInfoDb.getById(id);
    const favorite = !trackInfo?.favorite;
    localTrackInfoDb.updateFavorite(id, favorite);
    if (isCurrent) {
      activePlayerData.favorite = favorite;
      this.updateActivePlayerDataInDom();
      this.saveActivePlayerData();
    }
    this.callbacks.invokeFavorite({ id, favorite });
    if (window.isAuthenticated) {
      this.toggling[id] = true;
      this.sendToggleFavoriteRequest(id, favorite)
        .then((results: { favorite_track_ids: number[] }) => {
          const { favorite_track_ids } = results;
          localTrackInfoDb.updateFavoritesByTrackIds(favorite_track_ids);
          this.callbacks.invokeFavorites({
            favorites: favorite_track_ids,
          });
          const msgId = favorite ? 'trackAddedToFavorites' : 'trackRemovedFromFavorites';
          commonNotify.showSuccess(getJsText(msgId));
        })
        .catch((err) => {
          // eslint-disable-next-line no-console
          console.error('[FloatingPlayerClass:toggleFavoriteById] error', {
            err,
          });
          debugger; // eslint-disable-line no-debugger
          commonNotify.showError(err);
        })
        .finally(() => {
          this.toggling[id] = false;
        });
    }
  }

  seekPosition(position: number) {
    this.seeking = true;
    const audio = this.requireAudio();
    audio.currentTime = position || 0;
    this.state.position = position;
    this.updateTrackPosition();
    this.saveFloatingPlayerState();
    const activePlayerData = this.requireActivePlayerData();
    this.callbacks.invokeUpdate({ floatingPlayerState: this.state, activePlayerData });
    setTimeout(() => {
      this.seeking = false;
    }, 150);
  }

  seekRewind() {
    const position = Math.max(0, this.state.position - seekTimeSec);
    this.seekPosition(position);
  }

  seekForward() {
    const activePlayerData = this.requireActivePlayerData();
    const { duration } = activePlayerData;
    const position = Math.min(duration, this.state.position + seekTimeSec);
    this.seekPosition(position);
  }

  seekBarHandle(ev: Event) {
    const activePlayerData = this.requireActivePlayerData();
    const { duration } = activePlayerData;
    if (!duration) {
      return;
    }
    const node = ev.currentTarget as HTMLInputElement;
    const value = Number(node.value);
    const position = (value * duration) / 100;
    this.seekPosition(position);
    if (!this.isPlaying()) {
      this.playCurrentPlayer();
    }
  }

  // Initilization...

  initDomNode() {
    const domNode = this.requireDomNode();
    const seekBarNode = domNode.querySelector<HTMLInputElement>('.seekBar');
    if (seekBarNode) {
      seekBarNode.addEventListener('input', this.seekBarHandle.bind(this));
    }
    const hideButton = domNode.querySelector<HTMLButtonElement>('.track-control-hide');
    if (hideButton) {
      hideButton.addEventListener('click', this.hideFloatingPlayer.bind(this));
    }
    const controls = domNode.querySelectorAll<HTMLButtonElement>('.track-control');
    controls.forEach((node) => {
      const { dataset } = node;
      const { inited, controlId } = dataset;
      if (inited) {
        return;
      }
      if (controlId === 'rewind') {
        node.addEventListener('click', this.seekRewind.bind(this));
      }
      if (controlId === 'forward') {
        node.addEventListener('click', this.seekForward.bind(this));
      }
      if (controlId === 'toggleFavorite') {
        node.addEventListener('click', this.toggleFavorite.bind(this));
      }
      if (controlId === 'play') {
        node.addEventListener('click', this.trackPlayHandler.bind(this));
      }
      dataset.inited = TRUE;
    });
    this.inited = true;
  }
}
