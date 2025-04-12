import { floatingPlayer } from './entities/FloatingPlayer/floatingPlayer';
import { TrackInfo } from './track-blocks/TrackInfo';
import { localTrackInfoDb } from './track-blocks/localTrackInfoDb';

function onLogin() {
  const trackInfos: TrackInfo[] = localTrackInfoDb.getAll();
  console.log('[userSession:onLogin]', {
    trackInfos,
  });
  debugger;
  // TODO: Sync favorites and local tracks
}

function onLogout() {
  console.log('[userSession:onLogout]');
  // Clean favorites, local tracks
  localTrackInfoDb.clearAll();
  localTrackInfoDb.updateFavoritesByTrackIds([]);
  floatingPlayer.clearActivePlayerData();
  floatingPlayer.clearFloatingPlayerState();
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
