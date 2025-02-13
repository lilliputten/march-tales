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
  const list: (boolean | number)[] = JSON.parse(str);
  const [id, favorite, playedCount, position, lastUpdated, lastPlayed] = list;
  const trackInfo: TrackInfo = {
    id,
    favorite: Boolean(favorite),
    playedCount,
    position,
    lastUpdated,
    lastPlayed,
  } as TrackInfo;
  return trackInfo;
}

export function trackInfoToJsonStr(trackInfo: TrackInfo) {
  const { id, favorite, playedCount, position, lastUpdated, lastPlayed } = trackInfo;
  const list = [id, Number(favorite), playedCount, position, lastUpdated, lastPlayed];
  return JSON.stringify(list);
}
