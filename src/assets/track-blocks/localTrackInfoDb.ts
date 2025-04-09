import { TrackInfo, trackInfoFromJsonStr, trackInfoToJsonStr } from './TrackInfo';
import { setCookie } from '../helpers/CommonHelpers';
import { packDelim } from '../constants/packDelim';
import { acceptedCookiesId } from '../constants/acceptedCookiesId';

/* TODO: Use `new CustomEvent` to broadcast events */

class LocalTrackInfoDb {
  // End-user api

  updatePlayedCount(id: number, playedCount?: number, timestamp?: number) {
    try {
      const now = Date.now();
      const trackInfo = this.getOrCreate(id);
      if (playedCount == undefined || isNaN(playedCount)) {
        trackInfo.playedCount = trackInfo.playedCount ? trackInfo.playedCount + 1 : 1;
      } else {
        trackInfo.playedCount = playedCount;
      }
      trackInfo.lastPlayed = timestamp || now;
      trackInfo.lastUpdated = now;
      this.insert(trackInfo);
      // this.updateEvents.broadcast(TracksInfoDbUpdate(trackInfo));
      return trackInfo;
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error('[LocalTrackInfoDb:incrementPlayedCount]', err.message, {
        err,
        id,
      });
      debugger; // eslint-disable-line no-debugger
      throw err;
    }
  }

  updatePosition(id: number, position: number, timestamp?: number) {
    try {
      const now = Date.now();
      const trackInfo = this.getOrCreate(id);
      trackInfo.position = position;
      trackInfo.lastPlayed = timestamp || now; // ???
      trackInfo.lastUpdated = now;
      this.insert(trackInfo);
      // this.updateEvents.broadcast(TracksInfoDbUpdate(trackInfo));
      return trackInfo;
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error('[LocalTrackInfoDb:updatePosition]', err.message, {
        err,
        id,
      });
      debugger; // eslint-disable-line no-debugger
      throw err;
    }
  }

  updateFavorite(id: number, favorite: boolean, timestamp?: number) {
    try {
      const now = Date.now();
      const trackInfo = this.getOrCreate(id);
      trackInfo.favorite = favorite;
      trackInfo.lastFavorited = timestamp || now;
      trackInfo.lastUpdated = now;
      this.insert(trackInfo);
      this._toggleInFavoritesIndex(id, favorite);
      // this.updateEvents.broadcast(TracksInfoDbUpdate(trackInfo));
      return trackInfo;
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error('[LocalTrackInfoDb:setFavorite]', err.message, {
        err,
        id,
      });
      debugger; // eslint-disable-line no-debugger
      throw err;
    }
  }

  updateFavoritesByTrackIds(
    ids: number[],
    favoritedTimes?: Record<UserTrack['track_id'], UserTrack['favorited_at_sec']>,
    timestamp?: number,
  ) {
    const now = Date.now();
    const index = this._getIndex();
    index.forEach((id) => {
      const isFavorite = ids.includes(id);
      const trackInfo = this.getOrCreate(id);
      if (trackInfo.favorite !== isFavorite) {
        trackInfo.favorite = isFavorite;
        trackInfo.lastFavorited = (favoritedTimes && favoritedTimes[id]) || timestamp || now;
        // TODO: To check if it works correct
        trackInfo.lastUpdated = now;
        this.insert(trackInfo);
      }
    });
    this._setFavoritesIndex(ids);
  }

  save(trackInfo: TrackInfo, timestamp?: number) {
    try {
      const now = Date.now();
      trackInfo.lastPlayed = timestamp || now; // ???
      trackInfo.lastUpdated = now;
      this.insert(trackInfo);
      // this.updateEvents.broadcast(TracksInfoDbUpdate(trackInfo));
      // const testTrackInfo = await this.getById(id);
      return trackInfo;
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error('[LocalTrackInfoDb:save]', err.message, {
        err,
        trackInfo,
      });
      debugger; // eslint-disable-line no-debugger
      throw err;
    }
  }

  // Low-level api

  createNewRecord(id: number) {
    const now = Date.now();
    const trackInfo: TrackInfo = {
      id: id, // track.id
      favorite: false,
      playedCount: 0, // track.played_count (but only for current user!).
      position: 0, // position
      lastUpdated: now, // DateTime
      lastPlayed: 0, // DateTime
      lastFavorited: 0, // DateTime
    };
    return trackInfo;
  }

  getOrCreate(id: number) {
    return this.getById(id) || this.createNewRecord(id);
  }

  /// Create or update the record. (Returns inserted/updated record id.)
  insert(trackInfo: TrackInfo) {
    const { id } = trackInfo;
    const str = trackInfoToJsonStr(trackInfo);
    window.localStorage.setItem('ti-' + id, str);
    this._addToIndex(id);
  }

  getFavorites() {
    return this.getAll().filter((it) => it.favorite);
  }

  getById(id: number): TrackInfo | undefined {
    const str = window.localStorage.getItem('ti-' + id);
    if (!str) {
      return undefined;
    }
    return trackInfoFromJsonStr(str);
  }

  _getFavoritesIndex() {
    try {
      const str = window.localStorage.getItem('favorites');
      if (!str) {
        return [] as number[];
      }
      const list = str
        .split(packDelim)
        .map(Number)
        .filter((n) => !isNaN(n)) as number[];
      return list;
    } catch (
      _ // eslint-disable-line @typescript-eslint/no-unused-vars
    ) {
      return [] as number[];
    }
  }

  _setFavoritesIndex(favoritesIndex: number[]) {
    const list = favoritesIndex.filter((n) => !isNaN(n)).filter(Boolean);
    const str = list.join(packDelim);
    window.localStorage.setItem('favorites', str);
    // Update cookie value and document status
    const favoritesCount = list.length;
    const hasFavorites = !!favoritesCount;
    document.body.classList.toggle('has-favorites', hasFavorites);
    // Update count texts
    document.querySelectorAll<HTMLElement>('.favorites-count').forEach((node) => {
      node.innerText = String(favoritesCount);
    });
    // Update cookie
    if (window.localStorage.getItem(acceptedCookiesId)) {
      setCookie('favorites', str);
    }
  }

  _addToFavoritesIndex(id: number) {
    const favoritesIndex = this._getFavoritesIndex();
    if (!favoritesIndex.includes(id)) {
      favoritesIndex.push(id);
      this._setFavoritesIndex(favoritesIndex);
    }
  }

  _removeFromFavoritesIndex(id: number) {
    const favoritesIndex = this._getFavoritesIndex();
    if (favoritesIndex.includes(id)) {
      this._setFavoritesIndex(favoritesIndex.filter((checkId) => id !== checkId));
    }
  }

  _toggleInFavoritesIndex(id: number, value?: boolean) {
    if (value) {
      this._addToFavoritesIndex(id);
    } else {
      this._removeFromFavoritesIndex(id);
    }
  }

  _getIndex() {
    try {
      const str = window.localStorage.getItem('ti-index');
      return (str ? str.split(packDelim).map((v) => (v ? Number(v) : 0)) : []) as number[];
    } catch (
      _ // eslint-disable-line @typescript-eslint/no-unused-vars
    ) {
      return [] as number[];
    }
  }

  _setIndex(index: number[]) {
    window.localStorage.setItem('ti-index', index.join(packDelim));
  }

  _addToIndex(id: number) {
    const index = this._getIndex();
    if (!index.includes(id)) {
      index.push(id);
      this._setIndex(index);
    }
  }

  _removeFromIndex(id: number) {
    const index = this._getIndex();
    if (index.includes(id)) {
      this._setIndex(index.filter((checkId) => id !== checkId));
    }
  }

  _toggleInIndex(id: number, value?: boolean) {
    if (value) {
      this._addToIndex(id);
    } else {
      this._removeFromIndex(id);
    }
  }

  getAll() {
    const index = this._getIndex();
    const list: TrackInfo[] = index
      .map((id) => {
        return this.getById(id);
      })
      .filter(Boolean) as TrackInfo[];
    return list;
  }

  delete(id: number) {
    window.localStorage.removeItem('ti-' + id);
    this._removeFromIndex(id);
  }

  clearAll() {
    const index = this._getIndex();
    index.forEach((id) => {
      window.localStorage.removeItem('ti-' + id);
    });
    this._setIndex([]);
  }
}

// Create a singleton
export const localTrackInfoDb = new LocalTrackInfoDb();
