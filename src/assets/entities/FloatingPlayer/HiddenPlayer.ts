import { getJsText } from '../../helpers/getJsText';

interface THiddenPlayerOptions {
  type?: string;
  src?: string;
}

export class HiddenPlayer {
  hiddenPlayerNode?: HTMLElement;
  parentDomNode?: HTMLElement;

  audioNode?: HTMLAudioElement;
  sourceNode?: HTMLSourceElement;

  setParentDomNode(parentDomNode: HTMLElement) {
    this.parentDomNode = parentDomNode;
  }

  requireParentDomNode() {
    return this.parentDomNode || document.body;
  }

  ensureHiddenPlayer(/* opts: THiddenPlayerOptions = {} */) {
    if (!this.hiddenPlayerNode) {
      this.hiddenPlayerNode = document.createElement('div');
      this.hiddenPlayerNode.classList.add('hidden-player');
      const audio = document.createElement('audio');
      // audio.addEventListener('loadeddata', this.hiddenPlayerCanPlay);
      this.hiddenPlayerNode.appendChild(audio);
      const parentDomNode = this.requireParentDomNode();
      parentDomNode.appendChild(this.hiddenPlayerNode);
    }
    return this.hiddenPlayerNode;
  }

  hasAudio() {
    return !!this.audioNode;
  }

  hasSource() {
    return !!this.sourceNode;
  }

  ensureHiddenPlayerAudio() {
    if (!this.audioNode) {
      const parentDomNode = this.requireParentDomNode();
      this.audioNode = document.createElement('audio');
      this.audioNode.classList.add('hidden-player');
      this.audioNode.setAttribute('preload', 'auto');
      // audio.addEventListener('loadeddata', this.hiddenPlayerCanPlay);
      parentDomNode.appendChild(this.audioNode);
    }
    return this.audioNode;
  }

  createHiddenPlayerSource(opts: THiddenPlayerOptions = {}) {
    this.removeHiddenPlayerSource();
    const audio = this.ensureHiddenPlayerAudio();
    this.sourceNode = document.createElement('source');
    this.sourceNode.setAttribute('type', opts.type || 'audio/mpeg');
    if (opts.src) {
      this.sourceNode.setAttribute('src', opts.src);
    }
    // @see https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/loadeddata_event
    // audio.addEventListener('canplay', this.handleCanPlay.bind(this));
    // audio.addEventListener('playing', this.handlePlay.bind(this));
    // audio.addEventListener('timeupdate', this.handleTimeUpdate.bind(this));
    // audio.addEventListener('ended', this.handleEnded.bind(this));
    // this.sourceNode.addEventListener('error', this.handleError.bind(this));
    audio.appendChild(this.sourceNode);
    return this.sourceNode;
  }

  removeHiddenPlayerAudio() {
    if (this.audioNode) {
      this.audioNode.pause();
      this.audioNode.remove();
      this.audioNode = undefined;
      this.sourceNode = undefined;
    }
  }

  removeHiddenPlayerSource() {
    const audio = this.ensureHiddenPlayerAudio();
    const prevSources = Array.from(audio.getElementsByTagName('source'));
    for (const node of prevSources) {
      node.remove();
    }
    this.sourceNode = undefined;
  }
}
