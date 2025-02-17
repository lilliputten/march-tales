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
import {
  FloatingPlayerState,
  loadFloatingPlayerState,
  saveFloatingPlayerState,
} from './FloatingPlayerState';

import { HiddenPlayer } from './HiddenPlayer';

type ErrorCallback = (error: Error | string) => void;
// type TrackCallback = (activePlayerData: ActivePlayerData) => void;
type UpdateCallback = (
  floatingPlayerState: FloatingPlayerState,
  activePlayerData: ActivePlayerData,
) => void;

const TRUE = 'true';

// type HandlerId = 'play' | 'stop' | 'time';
export class FloatingPlayerCallbacks {
  onPlayStartCallbacks: UpdateCallback[] = [];
  onPlayStopCallbacks: UpdateCallback[] = [];
  onUpdateCallbacks: UpdateCallback[] = [];
  onErrorCallbacks: ErrorCallback[] = [];
  // handlers: Record<HandlerId, ErrorCallback[]> = {};

  addPlayStartCallback(cb: UpdateCallback) {
    if (cb && !this.onPlayStartCallbacks.includes(cb)) {
      this.onPlayStartCallbacks.push(cb);
    }
  }

  addPlayStopCallback(cb: UpdateCallback) {
    if (cb && !this.onPlayStopCallbacks.includes(cb)) {
      this.onPlayStopCallbacks.push(cb);
    }
  }

  addUpdateCallback(cb: UpdateCallback) {
    if (cb && !this.onUpdateCallbacks.includes(cb)) {
      this.onUpdateCallbacks.push(cb);
    }
  }

  addErrorCallback(cb: ErrorCallback) {
    if (cb && !this.onErrorCallbacks.includes(cb)) {
      this.onErrorCallbacks.push(cb);
    }
  }

  invokePlayStartCallbacks(
    floatingPlayerState: FloatingPlayerState,
    activePlayerData?: ActivePlayerData,
  ) {
    if (activePlayerData) {
      this.onPlayStartCallbacks.forEach((cb) => {
        cb(floatingPlayerState, activePlayerData);
      });
    }
  }

  invokePlayStopCallbacks(
    floatingPlayerState: FloatingPlayerState,
    activePlayerData?: ActivePlayerData,
  ) {
    if (activePlayerData) {
      this.onPlayStopCallbacks.forEach((cb) => {
        cb(floatingPlayerState, activePlayerData);
      });
    }
  }

  invokeUpdateCallbacks(
    floatingPlayerState: FloatingPlayerState,
    activePlayerData?: ActivePlayerData,
  ) {
    if (activePlayerData) {
      this.onUpdateCallbacks.forEach((cb) => {
        cb(floatingPlayerState, activePlayerData);
      });
    }
  }
  invokeErrorCallbacks(error: Error | string) {
    if (error) {
      this.onErrorCallbacks.forEach((cb) => {
        cb(error);
      });
    }
  }
}

export class FloatingPlayer {
  inited = false;
  callbacks = new FloatingPlayerCallbacks();
  audio?: HTMLAudioElement;
  hiddenPlayer: HiddenPlayer = new HiddenPlayer();
  activePlayerData?: ActivePlayerData;
  state: FloatingPlayerState = {};
  domNode?: HTMLElement;

  constructor() {
    this.loadActivePlayerData();
    this.loadFloatingPlayerState();
    this.initTrackDomNode();
    this.updateAll();
    // Check if it was recently playing...
    const now = Date.now();
    if (
      this.activePlayerData &&
      this.state.status === 'playing' &&
      this.state.lastTimestamp
      // && this.state.lastTimestamp > now - 5000
    ) {
      // TODO: Then resume playback...
      console.log('[FloatingPlayerClass:constructor] Start play', {
        activePlayerData: this.activePlayerData,
        state: this.state,
      });
      // TODO: Care about: `Uncaught (in promise) NotAllowedError: play() failed because the user didn't interact with the document first. https://goo.gl/xX8pDD`
      // this.playCurrentPlayer();
      // DEBUG: Temporarily remove the playing status
      // delete this.state.status;
    } else {
      // Reset the status
      delete this.state.status;
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

  // Hidden player...

  // Updaters...

  updateActivePlayerDataInDom() {
    const domNode = this.requireDomNode();
    const activePlayerData = this.requireActivePlayerData();
    const titleNode = domNode.querySelector<HTMLElement>('.title');
    titleNode.innerText = activePlayerData.title;
    const imageNode = domNode.querySelector<HTMLElement>('.image');
    imageNode.style.backgroundImage = 'url(' + activePlayerData.imageUrl + ')';
    // TODO: Ensure hidden player, set player url
  }

  updateStateInDom() {
    const domNode = this.requireDomNode();
    const { dataset } = domNode;
    if (this.state.status) {
      dataset.status = this.state.status;
    } else {
      delete dataset.status;
    }
    document.body.classList.toggle('withPlayer', !!this.state.visible);
  }

  updatePositionInDom() {
    const domNode = this.requireDomNode();
    const { dataset } = domNode;
    dataset.position = String(this.state.position || 0);
    dataset.progress = String(this.state.progress || 0);
    domNode.style.setProperty('--progress', String(this.state.progress || 0));
  }

  // setAudioPosition(position: number) {
  //   // audio.currentTime = position;
  // }

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
    const progress = Math.round(ratio * 100);
    return progress;
  }

  updateTrackPosition() {
    const domNode = this.requireDomNode();
    const timeNode = domNode.querySelector('.time');
    const activePlayerData = this.requireActivePlayerData();
    const { position } = this.state;
    const { id } = activePlayerData;
    const progress = this.calculateProgress();
    /* console.log('[FloatingPlayerClass:updateTrackPosition]', {
     *   id,
     *   position,
     *   progress,
     *   ratio,
     *   duration,
     *   timeNode,
     *   dataset,
     *   domNode,
     * });
     */
    this.state.progress = progress;
    this.updatePositionInDom();
    if (timeNode) {
      timeNode.innerHTML = formatDuration(Math.floor(position * 1000));
    }
    localTrackInfoDb.updatePosition(id, position);
  }

  // TODO: Update position
  // TODO: Update status

  updateAll() {
    this.updateStateInDom();
    this.updatePositionInDom();
    if (this.activePlayerData) {
      this.updateActivePlayerDataInDom();
    }
  }

  // Audio handlers...

  handleAudioTimeUpdate(ev: Event) {
    const currAudio = this.audio;
    const audio = ev.currentTarget as HTMLAudioElement;
    if (audio !== currAudio) {
      return;
    }
    const source = audio.getElementsByTagName('SOURCE')[0] as HTMLSourceElement;
    const { currentTime, readyState } = audio;
    const activePlayerData = this.requireActivePlayerData();
    console.log('[FloatingPlayerClass:handleAudioTimeUpdate]', {
      currentTime,
      readyState,
      id: activePlayerData.id,
      activePlayerData,
      src: source.src,
      source,
      thisAudio: currAudio === audio,
      currAudio,
      audio,
    });
    // TODO: Check loaded status?
    if (this.state.position != currentTime) {
      this.state.position = currentTime;
      this.updateTrackPosition();
      this.callbacks.invokeUpdateCallbacks(this.state, activePlayerData);
    }
  }

  handleAudioCanPlay(ev: Event) {
    if (!this.state.loaded) {
      const audio = ev.currentTarget as HTMLAudioElement;
      const source = audio.getElementsByTagName('SOURCE')[0] as HTMLSourceElement;
      const src = source?.src;
      console.log('[FloatingPlayerClass:sharedPlayerCanPlay]', {
        src,
        source,
        audio,
        ev,
      });
      this.state.loaded = true;
      delete this.state.error;
      // this.callbacks.invokeUpdateCallbacks(this.state, this.activePlayerData);
    }
  }

  handleAudioPlay(_ev: Event) {
    console.log('[FloatingPlayerClass:handleAudioPlay]');
    this.state.status = 'playing';
    this.updateStateInDom();
    this.saveFloatingPlayerState();
    this.callbacks.invokePlayStartCallbacks(this.state, this.activePlayerData);
  }

  handleAudioEnded(_ev: Event) {
    console.log('[FloatingPlayerClass:handleAudioEnded]');
    this.state.status = 'paused'; // stopped, ready?
    this.updateStateInDom();
    this.saveFloatingPlayerState();
    this.callbacks.invokePlayStopCallbacks(this.state, this.activePlayerData);
  }

  handleAudioSourceError(ev: Event) {
    const srcElement = ev.currentTarget as HTMLSourceElement;
    const { src, type } = srcElement;
    const errMsg = getJsText('errorLoadingAudioFile') + ' ' + src;
    const error = new Error(errMsg);
    // eslint-disable-next-line no-console
    console.error('[FloatingPlayerClass:handleAudioSourceError]', errMsg, {
      error,
      src,
      type,
      ev,
    });
    debugger; // eslint-disable-line no-debugger
    commonNotify.showError(errMsg);
    this.state.error = getErrorText(error);
    this.callbacks.invokeErrorCallbacks(error);
    // const dataset = currentTrackPlayer?.dataset;
    // if (dataset) {
    //   dataset.error = errMsg;
    //   delete dataset.loaded;
    //   delete dataset.status;
    // }
  }

  /// Active player data

  getActiveTrackId(): number | undefined {
    return this.activePlayerData ? this.activePlayerData.id : undefined;
  }

  // Core handlers...

  loadAudio() {
    // const domNode = this.requireDomNode();
    const activePlayerData = this.requireActivePlayerData();
    console.log('[FloatingPlayerClass:loadAudio]', {
      mediaUrl: activePlayerData.mediaUrl,
      id: activePlayerData.id,
    });
    this.state.loaded = false;
    const source = this.hiddenPlayer.createHiddenPlayerSource({ src: activePlayerData.mediaUrl });
    source.addEventListener('error', this.handleAudioSourceError.bind(this));
    // this.callbacks.invokeUpdateCallbacks(this.state, this.activePlayerData);
    // this.callbacks.invokePlayStartCallbacks(this.activePlayerData);
  }

  isAudioPlaying() {
    const audio = this.audio;
    return (
      !!audio && audio.currentTime > 0 && !audio.paused && !audio.ended && audio.readyState > 2
    );
  }

  isPlaying() {
    // TODO: Use audio node?
    // const audio = this.requireAudio()
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
      // this.callbacks.invokeUpdateCallbacks(this.state, this.activePlayerData);
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
      // audio.currentTime = 0;
      this.state.position = 0;
    }
    this.updateTrackPosition();
    this.callbacks.invokeUpdateCallbacks(this.state, this.activePlayerData);
    // if (!this.state.loaded || !this.hasAudio() || !this.hasAudioSource) {
    //   this.loadAudio();
    // }
    audio.currentTime = this.state.position || 0;
    audio.play();
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
      console.log('[FloatingPlayerClass:setActivePlayerData]', activePlayerData);
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

  setPosition(position?: number) {
    this.state.position = position;
    // ???
  }

  clearActiveData() {
    this.activePlayerData = undefined;
    this.hideFloatingPlayer();
    this.removeAudio();
  }

  // Initilization...

  initTrackDomNode() {
    const domNode = this.requireDomNode();
    const controls = domNode.querySelectorAll<HTMLElement>('.track-control');
    controls.forEach((node) => {
      const { dataset } = node;
      const { inited, controlId } = dataset;
      if (inited) {
        return;
      }
      // if (controlId === 'toggleFavorite') {
      //   node.addEventListener('click', toggleFavorite);
      // }
      if (controlId === 'play') {
        node.addEventListener('click', this.trackPlayHandler.bind(this));
      }
      dataset.inited = TRUE;
    });
    this.inited = true;
  }
}
