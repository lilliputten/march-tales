import { quoteHtmlAttr } from '../helpers/CommonHelpers';

export function getJsText(id: string) {
  const textNode = document.body.querySelector('#js-texts #' + id);
  if (!textNode) {
    // eslint-disable-next-line no-console
    console.warn('[getJsText] Can not find js text node for id:', id);
  }
  const text = textNode?.innerHTML || id;
  return quoteHtmlAttr(text).trim();
}
