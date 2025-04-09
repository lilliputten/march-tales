import { floatToStr } from '../helpers/floatToStr';
import { packDelim } from '../constants/packDelim';

export interface TrackInfo {
  id: number; // track.id
  favorite: boolean;
  playedCount: number; // track.played_count (but only for current user!).
  position: number; // position?.inMilliseconds ?? 0
  lastUpdated: number; // DateTime.now().millisecondsSinceEpoch <-> DateTime.fromMillisecondsSinceEpoch(ms)
  lastPlayed: number; // DateTime.now().millisecondsSinceEpoch <-> DateTime.fromMillisecondsSinceEpoch(ms)
  lastFavorited: number; // DateTime
}

const finalPackDelimReg = new RegExp(packDelim + '+$');

export function trackInfoFromJsonStr(str: string): TrackInfo | undefined {
  if (!str) {
    return undefined;
  }
  try {
    const list = str.split(packDelim);
    const [
      // Keep the order!
      id,
      favorite,
      playedCount,
      position,
      lastUpdated, // Timestamp
      lastPlayed, // Timestamp
      lastFavorited,
    ] = list;
    const data: TrackInfo = {
      // Keep the order!
      id: id ? Number(id) : 0,
      favorite: Boolean(favorite),
      playedCount: playedCount ? Number(playedCount) : 0,
      position: position ? Number(position) : 0,
      lastUpdated: lastUpdated ? Number(lastUpdated) * 1000 : 0, // Timestamp
      lastPlayed: lastPlayed ? Number(lastPlayed) * 1000 : 0, // Timestamp
      lastFavorited: lastFavorited ? Number(lastFavorited) * 1000 : 0, // Timestamp
    };
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
    lastFavorited,
  } = trackInfo;
  const list = [
    // Keep the order!
    id ? Number(id) : undefined,
    favorite ? Number(favorite) : undefined,
    playedCount ? Number(playedCount) : undefined,
    position ? floatToStr(position) : undefined, // Use fixed decimal presentation for floats
    lastUpdated ? Math.round(lastUpdated / 1000) : undefined, // Timestamp
    lastPlayed ? Math.round(lastPlayed / 1000) : undefined, // Timestamp
    lastFavorited ? Math.round(lastFavorited / 1000) : undefined, // Timestamp
  ];
  return list.join(packDelim).replace(finalPackDelimReg, '');
}
