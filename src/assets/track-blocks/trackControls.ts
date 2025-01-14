import { commonNotify } from '../CommonNotify/CommonNotifySingleton';
import { getCookie, quoteHtmlAttr } from '../helpers/CommonHelpers';

// Values for dataset statuses
const TRUE = 'true';

function getJsText(id: string) {
  const text = document.body.querySelector('#js-texts #' + id).innerHTML || id;
  return quoteHtmlAttr(text).trim();
}

function sendToggleFavoriteRequest(trackId: number | string, value: boolean) {
  const csrftoken = getCookie('csrftoken');
  const url = `/api/v1/tracks/${trackId}/toggle-favorite/`;
  const headers = {
    Accept: 'application/json',
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken,
    credentials: 'include',
    Cookie: csrftoken && `csrftoken=${csrftoken}`,
    sessionid: getCookie('sessionid'),
  };
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
      return data;
    });
}

function toggleFavorite(ev: Event) {
  const node = ev.currentTarget as HTMLElement;
  const controlsNode = node.closest('.track-controls') as HTMLElement;
  const { dataset } = controlsNode;
  const { trackId, favorite } = dataset;
  const value = !favorite;
  sendToggleFavoriteRequest(trackId, value)
    .then(() => {
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
