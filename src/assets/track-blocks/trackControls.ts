import { commonNotify } from '../CommonNotify/CommonNotifySingleton';
import { getJsText } from '../helpers/getJsText';
import { sendApiRequest } from '../helpers/sendApiRequest';

// Values for dataset statuses
const TRUE = 'true';

function sendToggleFavoriteRequest(trackId: number | string, value: boolean) {
  const url = `/api/v1/tracks/${trackId}/toggle-favorite/`;
  return sendApiRequest(url, 'POST', { value });
}

function toggleFavorite(ev: Event) {
  const node = ev.currentTarget as HTMLElement;
  const controlsNode = node.closest('.track-controls') as HTMLElement;
  const { dataset } = controlsNode;
  const { trackId, favorite } = dataset;
  const value = !favorite;
  sendToggleFavoriteRequest(trackId, value)
    .then((_results: { favorite_track_ids: number[] }) => {
      /* // DEBUG
       * const { favorite_track_ids } = results;
       * console.log('[trackControls:toggleFavorite]', {
       *   favorite_track_ids,
       * });
       */
      if (value) {
        dataset.favorite = TRUE;
        commonNotify.showSuccess(getJsText('trackAddedToFavorites'));
      } else {
        delete dataset.favorite;
        commonNotify.showSuccess(getJsText('trackRemovedFromFavorites'));
      }
    })
    .catch((err) => {
      // eslint-disable-next-line no-console
      console.error('[tracksPlayer:toggleFavorite:sendToggleFavoriteRequest] error', {
        err,
      });
      debugger; // eslint-disable-line no-debugger
      commonNotify.showError(err);
    });
}

function initTrackControlsNode(node: HTMLElement) {
  const { dataset } = node;
  const { inited, controlId } = dataset;
  if (inited) {
    return;
  }
  if (controlId === 'toggleFavorite') {
    node.addEventListener('click', toggleFavorite);
  }
  dataset.inited = TRUE;
}

export function initTrackControlsWrapper(domNode: HTMLElement = document.body) {
  const players = domNode.querySelectorAll(
    '.track-controls[data-track-id] .track-control[data-control-id]',
  );
  players.forEach(initTrackControlsNode);
}
