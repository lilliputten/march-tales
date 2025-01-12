import * as CommonHelpers from '../helpers/CommonHelpers';

/** Toast types */
type TMode = 'info' | 'error' | 'warn' | 'success';

/** Icon shapes (move to constants?) */
const icons: Record<TMode, string> = {
  success: 'bi-check',
  error: 'bi-exclamation-triangle-fill',
  warn: 'bi-bell-fill',
  info: 'bi-info-lg',
};

const iconClassNamePrefix = 'bi';

interface TNotifyData {
  node: HTMLDivElement;
  handler?: TSetTimeout;
}

// Define module...
class CommonNotify {
  notifyRoot: HTMLDivElement = undefined;

  timeoutDelay = 3000;

  inited = false;

  // Methods...

  removeNotify(notifyData: TNotifyData) {
    const { node, handler } = notifyData;
    // Play animation...
    node.classList.remove('active');
    if (handler) {
      clearTimeout(handler);
      notifyData.handler = undefined;
    }
    setTimeout(() => {
      // ...And remove node (TODO: Check if node still exists in dom tree)...
      try {
        this.notifyRoot.removeChild(node);
      } catch (
        _e // eslint-disable-line @typescript-eslint/no-unused-vars
      ) {
        // NOOP
      }
    }, 250); // Value of `var(--common-animation-time)`
  }

  /** showNotify
   * @param {'info' | 'error' | 'warn' | 'success'} mode - Message type ('info' is default)
   * @param {string|Error} text - Message content
   */
  showNotify(mode: TMode, text: string | Error) {
    this.ensureInit();
    if (!text) {
      // If only one parameters passed assume it as message with default type
      text = mode;
      mode = 'info';
    }
    let content: string;
    if (text instanceof Error) {
      // Convert error object to the plain text...
      content = CommonHelpers.getErrorText(text);
    } else {
      content = String(text);
    }
    // Create node...
    const node = document.createElement('div');
    node.classList.add('notify');
    node.classList.add('notify-' + mode);
    // Add icon...
    const nodeIcon = document.createElement('span');
    nodeIcon.classList.add('icon');
    nodeIcon.classList.add(iconClassNamePrefix);
    nodeIcon.classList.add(icons[mode]);
    node.appendChild(nodeIcon);
    // Add text...
    const nodeText = document.createElement('div');
    nodeText.classList.add('text');
    nodeText.innerHTML = content;
    node.appendChild(nodeText);
    this.notifyRoot.appendChild(node);
    // Play appearing animation...
    window.requestAnimationFrame(() => {
      setTimeout(() => {
        node.classList.add('active');
      }, 10);
    });
    // Remove node after delay...
    /** @type {TNotifyData} */
    const notifyData: TNotifyData = { node, handler: undefined };
    const removeNotifyHandler = this.removeNotify.bind(this, notifyData);
    notifyData.handler = setTimeout(removeNotifyHandler, this.timeoutDelay);
    // Stop & restore timer on mouse in and out events...
    node.addEventListener('mouseenter', () => {
      // Clear timer...
      clearTimeout(notifyData.handler);
    });
    node.addEventListener('mouseleave', () => {
      // Resume timer...
      notifyData.handler = setTimeout(removeNotifyHandler, this.timeoutDelay);
    });
    // Click handler...
    node.addEventListener('click', removeNotifyHandler);
  }

  // Some shorthands...

  /** @param {string|Error} text - Message content */
  showInfo(text: string | Error) {
    this.showNotify('info', text);
  }

  /** @param {string|Error} text - Message content */
  showSuccess(text: string | Error) {
    this.showNotify('success', text);
  }

  /** @param {string|Error} text - Message content */
  showWarn(text: string | Error) {
    this.showNotify('warn', text);
  }

  /** @param {string|Error} text - Message content */
  showError(text: string | Error) {
    this.showNotify('error', text);
  }

  // Demo...

  showDemo() {
    // DEBUG: Show sample notifiers...
    this.showInfo('Info');
    this.showSuccess('Success');
    this.showWarn('Warn');
    this.showError('Error');
  }

  // Initialization...

  /** Ensure the modal has initiazlized */
  ensureInit() {
    this.init();
  }

  createDomNode() {
    // TODO: To use bootstrap toasts?
    const rootNode = document.body;
    const notifyRoot = document.createElement('div');
    notifyRoot.classList.add('notify-root');
    notifyRoot.setAttribute('id', 'notify-root');
    rootNode.appendChild(notifyRoot);
    this.notifyRoot = notifyRoot;
  }

  /** Initialize nodule. */
  init() {
    if (!this.inited) {
      this.createDomNode();
      this.inited = true;
    }
  }
}

// Create and export singletone
export const commonNotify = new CommonNotify();

// commonNotify.init();
