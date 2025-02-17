import { ActivePlayerData } from '../ActivePlayerData/ActivePlayerData';
import { FloatingPlayerState } from './FloatingPlayerState';

export interface FloatingPlayerUpdateData {
  floatingPlayerState: FloatingPlayerState;
  activePlayerData: ActivePlayerData;
}
export interface FloatingPlayerIncrementData {
  count?: number;
  // floatingPlayerState: FloatingPlayerState;
  activePlayerData: ActivePlayerData;
}
type UpdateCallback = (data: FloatingPlayerUpdateData) => void;
type IncrementCallback = (data: FloatingPlayerIncrementData) => void;
type ErrorCallback = (error: Error | string) => void;

// type HandlerId = 'play' | 'stop' | 'time';
export class FloatingPlayerCallbacks {
  onPlayStartCallbacks: UpdateCallback[] = [];
  onPlayStopCallbacks: UpdateCallback[] = [];
  onUpdateCallbacks: UpdateCallback[] = [];
  onIncrementCallbacks: IncrementCallback[] = [];
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

  addIncrementCallback(cb: IncrementCallback) {
    if (cb && !this.onIncrementCallbacks.includes(cb)) {
      this.onIncrementCallbacks.push(cb);
    }
  }

  addErrorCallback(cb: ErrorCallback) {
    if (cb && !this.onErrorCallbacks.includes(cb)) {
      this.onErrorCallbacks.push(cb);
    }
  }

  // Invokers

  invokePlayStart(data: FloatingPlayerUpdateData) {
    if (data.activePlayerData) {
      this.onPlayStartCallbacks.forEach((cb) => {
        cb(data);
      });
    }
  }

  invokePlayStop(data: FloatingPlayerUpdateData) {
    if (data.activePlayerData) {
      this.onPlayStopCallbacks.forEach((cb) => {
        cb(data);
      });
    }
  }

  invokeUpdate(data: FloatingPlayerUpdateData) {
    if (data.activePlayerData) {
      this.onUpdateCallbacks.forEach((cb) => {
        cb(data);
      });
    }
  }

  invokeIncrement(data: FloatingPlayerIncrementData) {
    if (data.activePlayerData) {
      this.onIncrementCallbacks.forEach((cb) => {
        cb(data);
      });
    }
  }
  invokeError(error: Error | string) {
    if (error) {
      this.onErrorCallbacks.forEach((cb) => {
        cb(error);
      });
    }
  }
}
