import { floatToStr } from '../helpers/floatToStr';

export interface TrackInfo {
  id: number; // track.id
  favorite: boolean;
  playedCount: number; // track.played_count (but only for current user!).
  position: number; // position?.inMilliseconds ?? 0
  lastUpdated: number; // DateTime.now().millisecondsSinceEpoch <-> DateTime.fromMillisecondsSinceEpoch(ms)
  lastPlayed: number; // DateTime.now().millisecondsSinceEpoch <-> DateTime.fromMillisecondsSinceEpoch(ms)
}

export function trackInfoFromJsonStr(str: string) {
  if (!str) {
    return undefined;
  }
  try {
    const list = str.split(',');
    const [
      // Keep the order!
      id,
      favorite,
      playedCount,
      position,
      lastUpdated,
      lastPlayed,
    ] = list;
    const data: TrackInfo = {
      // Keep the order!
      id: id ? Number(id) : 0,
      favorite: Boolean(favorite),
      playedCount: playedCount ? Number(playedCount) : 0,
      position: position ? Number(position) : 0,
      lastUpdated: lastUpdated ? Number(lastUpdated) : 0,
      lastPlayed: lastPlayed ? Number(lastPlayed) : 0,
    };
    /* console.log('[TrackInfo:trackInfoFromJsonStr]', {
     *   str,
     *   data,
     * });
     */
    return data;
  } catch (
    err // eslint-disable-line @typescript-eslint/no-unused-vars
  ) {
    // eslint-disable-next-line no-console
    console.warn('[TrackInfo:trackInfoFromJsonStr] Parse error', {
      str,
      err,
    });
    return undefined;
  }
}

export function trackInfoToJsonStr(trackInfo: TrackInfo) {
  const {
    // Keep the order!
    id,
    favorite,
    playedCount,
    position,
    lastUpdated,
    lastPlayed,
  } = trackInfo;
  const list = [
    // Keep the order!
    id ? Number(id) : undefined,
    favorite ? Number(favorite) : undefined,
    playedCount ? Number(playedCount) : undefined,
    position ? floatToStr(position) : undefined, // Use fixed decimal presentation for floats
    lastUpdated ? Number(lastUpdated) : undefined,
    lastPlayed ? Number(lastPlayed) : undefined,
  ];
  return list.join(',').replace(/,+$/, '');
}
