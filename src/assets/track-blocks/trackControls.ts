import { commonNotify } from '../CommonNotify/CommonNotifySingleton';
import { getCookie } from '../helpers/CommonHelpers';

// Values for dataset statuses
const TRUE = 'true';

function sendToggleFavoriteRequest(trackId: number | string, value: boolean) {
  const csrfToken = getCookie('csrftoken');
  const url = `/api/api-tracks/${trackId}/toggleFavorite/`;
  const headers = {
    Accept: 'application/json',
    'Content-Type': 'application/json',
    'X-CSRFToken': csrfToken,
  };
  /* console.log('[tracksPlayer:sendToggleFavoriteRequest] star', {
   *   url,
   *   headers,
   *   csrfToken,
   *   trackId,
   * });
   */
  return fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      value,
    }),
  })
    .then(async (res) => {
      const data = await res.json();
      return [res, data];
    })
    .then(([res, data]: [Response, { detail?: string }]) => {
      const { ok, status } = res;
      if (!ok) {
        const errMsg = [`Error ${status}`, data?.detail || res.statusText]
          .filter(Boolean)
          .join(': ');
        throw new Error(errMsg);
      }
      /* console.log('[tracksPlayer:sendToggleFavoriteRequest] success', {
       *   data,
       * });
       */
      return data;
    });
}

function toggleFavorite(ev: Event) {
  const node = ev.currentTarget as HTMLElement;
  // const { controlId } = node.dataset;
  const controlsNode = node.closest('.track-controls') as HTMLElement;
  const { dataset } = controlsNode;
  const { trackId, favorite } = dataset;
  const value = !favorite;
  /* console.log('[toggleFavorite]', {
   *   // controlId,
   *   value,
   *   favorite,
   *   trackId,
   *   controlsNode,
   *   node,
   * });
   */
  sendToggleFavoriteRequest(trackId, value)
    .then(() => {
      /* console.log('[trackControls:toggleFavorite:sendToggleFavoriteRequest]', {
       *   value,
       * });
       */
      if (value) {
        dataset.favorite = TRUE;
      } else {
        delete dataset.favorite;
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
