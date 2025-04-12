import { ActivePlayerData } from '../ActivePlayerData/ActivePlayerData';
import { FloatingPlayerState } from './FloatingPlayerState';

export interface FloatingPlayerUpdateData {
  floatingPlayerState: FloatingPlayerState;
  activePlayerData: ActivePlayerData;
}
export interface FloatingPlayerIncrementData {
  count?: number;
  activePlayerData: ActivePlayerData;
}
export interface FloatingPlayerFavoritesData {
  favorites: number[];
}
export interface FloatingPlayerFavoriteData {
  id: number;
  favorite: boolean;
}
type UpdateCallback = (data: FloatingPlayerUpdateData) => void;
type IncrementCallback = (data: FloatingPlayerIncrementData) => void;
type FavoritesCallback = (data: FloatingPlayerFavoritesData) => void;
type FavoriteCallback = (data: FloatingPlayerFavoriteData) => void;
type ErrorCallback = (error: Error | string) => void;

export class FloatingPlayerCallbacks {
  onPlayStartCallbacks: UpdateCallback[] = [];
  onPlayStopCallbacks: UpdateCallback[] = [];
  onUpdateCallbacks: UpdateCallback[] = [];
  onIncrementCallbacks: IncrementCallback[] = [];
  onFavoritesCallbacks: FavoritesCallback[] = [];
  onFavoriteCallbacks: FavoriteCallback[] = [];
  onErrorCallbacks: ErrorCallback[] = [];

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

  addFavoriteCallback(cb: FavoriteCallback) {
    if (cb && !this.onFavoriteCallbacks.includes(cb)) {
      this.onFavoriteCallbacks.push(cb);
    }
  }

  addFavoritesCallback(cb: FavoritesCallback) {
    if (cb && !this.onFavoritesCallbacks.includes(cb)) {
      this.onFavoritesCallbacks.push(cb);
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

  invokeFavorite(data: FloatingPlayerFavoriteData) {
    this.onFavoriteCallbacks.forEach((cb) => {
      cb(data);
    });
  }

  invokeFavorites(data: FloatingPlayerFavoritesData) {
    this.onFavoritesCallbacks.forEach((cb) => {
      cb(data);
    });
  }

  invokeError(error: Error | string) {
    if (error) {
      this.onErrorCallbacks.forEach((cb) => {
        cb(error);
      });
    }
  }
}
