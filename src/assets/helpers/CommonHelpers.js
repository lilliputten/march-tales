// @ts-check

export function NOOP() {}

/** Compare two arrays with scalar (number, string, boolean) values
 * @param {(number | string | boolean)[]} a1
 * @param {(number | string | boolean)[]} a2
 * @return {boolean}
 */
export function compareArrays(a1, a2) {
  if (!a1 || !a1) {
    return a1 === a2;
  }
  if (a1.length !== a2.length) {
    return false;
  }
  // Compare all the items...
  for (let i = 0; i < a1.length; i++) {
    if (a1[i] !== a2[i]) {
      return false;
    }
  }
  return true;
}

/** getErrorText - Return plain text for error.
 * @param {string|Error|string[]|Error[]} error - Error or errors list.
 * @return {string}
 */
export function getErrorText(error) {
  if (!error) {
    return '';
  }
  if (Array.isArray(error)) {
    return error.map(this.getErrorText.bind(this)).join('\n');
  }
  if (error instanceof Error) {
    error = error.message;
  } else if (typeof error !== 'string') {
    // TODO?
    error = String(error);
  }
  return error;
}

/** quoteHtmlAttr -- quote all invalid characters for html
 * @param {string} str
 * @param {boolean} [preserveCR]
 */
export function quoteHtmlAttr(str, preserveCR) {
  const crValue = preserveCR ? '&#13;' : '\n';
  return (
    String(str) // Forces the conversion to string
      .replace(/&/g, '&amp;') // This MUST be the 1st replacement
      .replace(/'/g, '&apos;') // The 4 other predefined entities, required
      .replace(/"/g, '&quot;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      // You may add other replacements here for HTML only (but it's not
      // necessary). Or for XML, only if the named entities are defined in its
      // DTD.
      .replace(/\r\n/g, crValue) // Must be before the next replacement
      .replace(/[\r\n]/g, crValue)
  );
}

/** htmlToElement -- Create dom node instance from html string
 * @param {string} html - Html representing a single element
 * @return {HTMLElement}
 */
export function htmlToElement(html) {
  const template = document.createElement('template');
  if (Array.isArray(html)) {
    html = html.join('');
  }
  html = html.trim(); // Never return a text node of whitespace as the result
  template.innerHTML = html;
  const content = template.content;
  return /** @type HTMLElement */ (content.firstChild);
}

/** htmlToElements -- Convert text html representation to HTMLCollection object
 * @param {string|string[]} html
 * @return {HTMLCollection}
 */
export function htmlToElements(html) {
  const template = document.createElement('template');
  if (Array.isArray(html)) {
    html = html.join('');
  }
  html = html.trim(); // Never return a text node of whitespace as the result
  template.innerHTML = html;
  const content = template.content;
  return content.children;
}

/** updateNodeContent -- Replace all inner dom node content.
 * @param {Element} node
 * @param {THtmlContent} content
 */
export function updateNodeContent(node, content) {
  if (!node) {
    throw new Error('Undefined node to update content');
  }
  if (typeof content === 'string') {
    // Replace with string content...
    node.innerHTML = content;
  } else if (Array.isArray(content)) {
    // Replace multiple elements...
    node.replaceChildren.apply(node, content);
  } else {
    // Replace single element...
    node.replaceChildren(content);
  }
}

/** decodeQuery
 * @param {string | string[]} qs
 * @param {string} [sep]
 * @param {string} [eq]
 * @param {any} [options]
 * @returns {{}}
 */
export function decodeQuery(qs, sep, eq, options) {
  sep = sep || '&';
  eq = eq || '=';
  /** @type {Record<string, unknown> | unknown[]} */
  const obj = {};
  if (typeof qs !== 'string' || qs.length === 0) {
    return obj;
  }
  const regexp = /\+/g;
  qs = qs.split(sep);
  let maxKeys = 1000;
  if (options && typeof options.maxKeys === 'number') {
    maxKeys = options.maxKeys;
  }
  let len = qs.length;
  // maxKeys <= 0 means that we should not limit keys count
  if (maxKeys > 0 && len > maxKeys) {
    len = maxKeys;
  }
  for (let i = 0; i < len; ++i) {
    const x = qs[i].replace(regexp, '%20'),
      idx = x.indexOf(eq);
    let kstr, vstr;
    if (idx >= 0) {
      kstr = x.substring(0, idx);
      vstr = x.substring(idx + 1);
    } else {
      kstr = x;
      vstr = '';
    }
    const k = decodeURIComponent(kstr);
    const v = decodeURIComponent(vstr);
    const it = obj[k];
    if (!Object.prototype.hasOwnProperty.call(obj, k)) {
      obj[k] = v;
    } else if (Array.isArray(it)) {
      it.push(v);
    } else {
      obj[k] = [it, v];
    }
  }
  return obj;
}

/** parseQuery -- Parse url query string (in form `?xx=yy&...` or `xx=yy&...`)
 * @param {string} search  - Query string
 * @return {Record<string, string>} query - Query object
 */
export function parseQuery(search) {
  if (!search) {
    return {};
  }
  if (search.indexOf('?') === 0) {
    search = search.substring(1);
  }
  return decodeQuery(search);
}

/** makeQuery
 * @param {Record<string, string | number | boolean> | {}} params
 * @param {{ addQuestionSymbol?: boolean; useEmptyStrings?: boolean; useUndefinedValues?: boolean }} opts
 * @returns {string}
 */
export function makeQuery(params, opts = {}) {
  let url = Object.entries(params)
    .map(([id, val]) => {
      const valStr = String(val);
      if (val == undefined && !opts.useUndefinedValues) {
        return undefined;
      }
      if (valStr === '' && !opts.useEmptyStrings) {
        return undefined;
      }
      return encodeURI(id) + '=' + encodeURI(String(val == undefined ? '' : val));
    })
    .filter(Boolean)
    .join('&');
  if (opts.addQuestionSymbol && url) {
    url = '?' + url;
  }
  return url;
}

/** Dynamically load external script
 * @param {string} url
 * @return {Promise<Event>}
 */
export function addScript(url) {
  return new Promise((resolve, reject) => {
    // document.write('<script src="' + url + '"></script>');
    const script = document.createElement('script');
    script.setAttribute('src', url);
    script.addEventListener('load', resolve);
    script.addEventListener('error', (event) => {
      const {
        target,
        // srcElement,
      } = event;
      // @ts-ignore
      const { href, baseURI } = target;
      const error = new Error(`Cannot load script resurce by url '${url}'`);
      // eslint-disable-next-line no-console
      console.error('[CommonHelpers:addScript]', {
        error,
        url,
        href,
        baseURI,
        target,
        event,
      });
      // eslint-disable-next-line no-debugger
      debugger;
      reject(error);
    });
    document.head.appendChild(script);
  });
}

/** Dynamically load external css
 * @param {string} url
 * @return {Promise<unknown>}
 */
export function addCssStyle(url) {
  return new Promise((resolve, reject) => {
    // Try to find exists node...
    const testNode = document.head.querySelector(
      'link[href="' + url + '"], link[data-url="' + url + '"]',
    );
    if (testNode) {
      // Style already found!
      return resolve({ type: 'already-loaded', target: testNode });
    }
    // reject(new Error('test')); // DEBUG: Test errors catching
    const node = document.createElement('link');
    node.setAttribute('href', url);
    node.setAttribute('type', 'text/css');
    node.setAttribute('rel', 'stylesheet');
    node.setAttribute('data-url', url);
    node.addEventListener('load', resolve);
    node.addEventListener('error', (event) => {
      const {
        target,
        // srcElement,
      } = event;
      // @ts-ignore
      const { href, baseURI } = target;
      const error = new Error(`Cannot load css resurce by url '${url}'`);
      // eslint-disable-next-line no-console
      console.error('[CommonHelpers:addCssStyle]', {
        error,
        url,
        href,
        baseURI,
        target,
        event,
      });
      // eslint-disable-next-line no-debugger
      debugger;
      reject(error);
    });
    document.head.appendChild(node);
  });
}

/**
 * @param {HTMLSelectElement} node
 * @param {(string|number)[]} values
 */
export function setMultipleSelectValues(node, values) {
  const strValues = values.map(String);
  const options = Array.from(node.options);
  options.forEach((item) => {
    const { value, selected } = item;
    const isSelected = strValues.includes(value);
    if (isSelected !== selected) {
      item.selected = isSelected;
    }
  });
}

/** processMultipleRequestErrors
 * @param {Response[]} resList
 * @return {Error[]}
 */
export function processMultipleRequestErrors(resList) {
  return /** @type {Error[]} */ (
    resList
      .map((res) => {
        if (!res.ok) {
          return new Error(`Can't load url '${res.url}': ${res.statusText}, ${res.status}`);
        }
      })
      .filter(Boolean)
  );
}

/**
 * @param {number} n
 * @param {TNormalizedFloatStrOptions} [opts={}]
 * @returns {string}
 */
export function normalizedFloatStr(n, opts = {}) {
  const {
    // prettier-ignore
    fixedPoint = 2,
    stripFixedZeros = true,
  } = opts;
  let str = n.toFixed(fixedPoint);
  if (stripFixedZeros) {
    str = str.replace(/\.*0+$/, '');
  }
  return str;
}
/**
 * @param {number} size
 * @param {TGetApproxSizeOptions} [opts={}]
 * @returns {[number | string, string]}
 */
export function getApproxSize(size, opts = {}) {
  const { normalize } = opts;
  const levels = [
    'B', // Bytes
    'K', // Kilobytes
    'M', // Megabytes
    'G', // Gigabites
  ];
  const lastLevel = levels.length - 1;
  const range = 1024;
  let level = 0;
  while (level < lastLevel) {
    if (size < range) {
      break;
    }
    size /= range;
    level++;
  }
  const currLevelStr = levels[level];
  /** Result: final number or normalized representation (depends on option's `normalize`)
   * @type {number | string}
   */
  let result = size;
  if (normalize) {
    const normalizeOpts = typeof normalize === 'object' ? normalize : undefined;
    result = normalizedFloatStr(size, normalizeOpts);
  }
  return [result, currLevelStr];
}

/** @param {number} time - Time duration, ms
 * @return {string}
 */
export function formatDuration(time) {
  const sec = time / 1000;
  const min = sec / 60;
  const hrs = min / 60;
  const days = hrs / 24;
  const srcItems = [
    // prettier-ignore
    days,
    hrs % 24,
    min % 60,
    sec % 60,
  ];
  const items = srcItems.map(Math.floor).map((val, idx) => {
    // Not mins and secs and empty...
    if (idx < 2 && !val) {
      return undefined;
    }
    // Hours, mins, secs...
    if (idx >= 1) {
      return String(val).padStart(2, '0');
    }
    // Days...
    if (!idx) {
      return String(val) + 'd';
    }
  });
  /* console.log('[CommonHelpers:formatDuration]', {
   *   sec,
   *   min,
   *   hrs,
   *   days,
   *   items,
   *   srcItems,
   *   time,
   * });
   */
  const daysStr = items.shift();
  return [
    // prettier-ignore
    daysStr,
    items.filter(Boolean).join(':'),
  ]
    .filter(Boolean)
    .join(' ');
}

/** @param {string} str */
export function getAsyncHash(str) {
  const encoder = new TextEncoder();
  const buf = encoder.encode(str);
  return crypto.subtle.digest('SHA-256', buf).then((aryBuf) => {
    const ary = new Uint8Array(aryBuf);
    const res = Array.from(ary)
      .map((x) => x.toString(16).padStart(2, '0'))
      .join('');
    return res;
  });
}

/** @param {string} cookieId */
export function getCookie(cookieId) {
  const cookiesStr = document.cookie;
  const cookiesList = cookiesStr.split(';'); // .map((s) => s.trim().split('='));
  for (let i = 0; i < cookiesList.length; i++) {
    const s = cookiesList[i];
    const [id, val] = s.trim().split('=').map(decodeURIComponent);
    if (id === cookieId) {
      return val;
    }
  }
  return undefined;
}

/**
 * @param {string} id
 * @param {string} val
 * @param {number} [maxAgeSecs] -- Seconds of expire period
 */
export function setCookie(id, val, maxAgeSecs) {
  const cookieVal = [id, val || ''].map(encodeURIComponent).join('=');
  const parts = [
    // prettier-ignore
    cookieVal,
    'path=/',
  ];
  if (maxAgeSecs) {
    parts.push('max-age=' + maxAgeSecs);
  }
  const fullCookie = parts.filter(Boolean).join(';');
  document.cookie = fullCookie;
}

export function deleteAllCookies() {
  document.cookie.split(';').forEach((cookie) => {
    const eqPos = cookie.indexOf('=');
    const name = eqPos > -1 ? cookie.substring(0, eqPos) : cookie;
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT';
  });
}
