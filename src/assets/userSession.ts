import { commonNotify } from './CommonNotify/CommonNotifySingleton';
import { floatingPlayer } from './entities/FloatingPlayer/floatingPlayer';
import { sendApiRequest } from './helpers/sendApiRequest';
import { TrackInfo } from './track-blocks/TrackInfo';
import { localTrackInfoDb } from './track-blocks/localTrackInfoDb';

function createUserTrackFromTrackInfo(trackInfo: TrackInfo) {
  /* if (!window.userId) {
   *   throw new Error('No user defined');
   * }
   */
  const userTrack: Partial<UserTrack> = {
    // id, // number
    // user_id: window.userId, // number
    track_id: trackInfo.id, // number
    is_favorite: trackInfo.favorite, // number
    // played_count: trackInfo.localPlayedCount, // number, Should we update user's own played count on the server?
    position: trackInfo.position, // number
    favorited_at_sec: Math.round(trackInfo.lastFavorited / 1000), // number, DateTime, in seconds
    played_at_sec: Math.round(trackInfo.lastPlayed / 1000), // number, DateTime, in seconds
    updated_at_sec: Math.round(trackInfo.lastUpdated / 1000), // number, DateTime, in seconds
  };
  return userTrack;
}

function sendSyncUserTracksRequest(items: Partial<UserTrack>[]) {
  // TODO: Sync favorites and local tracks..
  const url = `/api/v1/user/tracks/sync/`;
  const data = {
    items,
  };
  /* console.log('[userSession:sendSyncUserTracksRequest] start', {
   *   items,
   *   url,
   * });
   */
  return sendApiRequest(url, 'POST', data)
    .then((_result: { updated_items: UserTrack[] }) => {
      /* const updatedUserTracks = result.updated_items;
       * // TODO: Update local data with returned data?
       * console.log('[userSession:sendSyncUserTracksRequest] done', {
       *   updatedUserTracks,
       * });
       */
    })
    .catch((err) => {
      // eslint-disable-next-line no-console
      console.error('[userSession:sendSyncUserTracksRequest] error', {
        err,
      });
      debugger; // eslint-disable-line no-debugger
      commonNotify.showError(err);
    });
}

function onLogin() {
  if (window.localStorage) {
    if (window.localStorage.getItem('logged')) {
      // return;
    }
    window.localStorage.setItem('logged', 'yes');
  }
  const trackInfos: TrackInfo[] = localTrackInfoDb.getAll();
  const userTracks: Partial<UserTrack>[] = trackInfos.map(createUserTrackFromTrackInfo);
  // Sync favorites and local tracks...
  sendSyncUserTracksRequest(userTracks);
  // console.log('[userSession:onLogin]');
}

function onLogout() {
  if (window.localStorage) {
    if (!window.localStorage.getItem('logged')) {
      return;
    }
    window.localStorage.removeItem('logged');
  }
  // Clean favorites, local tracks
  localTrackInfoDb.clearAll();
  localTrackInfoDb.updateFavoritesByTrackIds([]);
  floatingPlayer.clearActivePlayerData();
  floatingPlayer.clearFloatingPlayerState();
  // console.log('[userSession:onLogout]');
}

export function userSession() {
  const bodyNode = document.body;
  const isLogin = bodyNode.classList.contains('login_success');
  const isLogout = bodyNode.classList.contains('logged_out');
  if (isLogin) {
    onLogin();
  } else if (isLogout) {
    onLogout();
  }
}
