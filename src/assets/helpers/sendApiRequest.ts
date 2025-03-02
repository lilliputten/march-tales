import { getCookie } from '../helpers/CommonHelpers';
import * as CommonHelpers from '../helpers/CommonHelpers';
import { getJsText } from './getJsText';

export function sendApiRequest(url: string, method: string = 'GET', requestData?: unknown) {
  const csrftoken = getCookie('csrftoken');
  const headers = {
    Accept: 'application/json',
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken || '',
    // Credentials: 'include',
    // Cookie: csrftoken && `csrftoken=${csrftoken}`,
    // 'X-Session-Token': sessionId, // X-Session-Token
    // 'Accept-Language': 'ru', // django_language=ru; content-language: ru;
  };
  return fetch(url, {
    method,
    headers,
    credentials: 'include',
    body: requestData ? JSON.stringify(requestData) : null,
  })
    .then(async (res) => {
      const { ok, status, statusText } = res;
      // TODO: Check is it json?
      let data: (unknown & { detail?: string }) | undefined = undefined;
      try {
        data = await res.json();
      } catch (
        _e // eslint-disable-line @typescript-eslint/no-unused-vars
      ) {
        // NOOP
      }
      if (!ok || status !== 200) {
        const errMsg = [getJsText('fetchError') + ' ' + status, data?.detail || statusText]
          .filter(Boolean)
          .join(': ');
        // eslint-disable-next-line no-console
        console.error('[sendApiRequest]', errMsg, {
          ok,
          data,
          statusText,
          status,
          res,
          url,
          requestData,
          method,
          headers,
        });
        debugger; // eslint-disable-line no-debugger
        throw new Error(errMsg);
      }
      return data as unknown;
    })
    .catch((err) => {
      const errMsg = [getJsText('failedApiRequest'), CommonHelpers.getErrorText(err)]
        .filter(Boolean)
        .join(': ');
      // eslint-disable-next-line no-console
      console.error('[sendApiRequest]', errMsg, {
        err,
        url,
        requestData,
        method,
        headers,
      });
      debugger; // eslint-disable-line no-debugger
      throw new Error(errMsg);
    });
}
