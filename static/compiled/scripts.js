/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./src/assets/CommonNotify/CommonNotifySingleton.ts":
/*!**********************************************************!*\
  !*** ./src/assets/CommonNotify/CommonNotifySingleton.ts ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   commonNotify: () => (/* binding */ commonNotify)
/* harmony export */ });
/* harmony import */ var _helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../helpers/CommonHelpers */ "./src/assets/helpers/CommonHelpers.js");

/** Icon shapes (move to constants?) */
var icons = {
    success: 'bi-check',
    error: 'bi-exclamation-triangle-fill',
    warn: 'bi-bell-fill',
    info: 'bi-info-lg',
};
var iconClassNamePrefix = 'bi';
// Define module...
var CommonNotify = /** @class */ (function () {
    function CommonNotify() {
        this.timeoutDelay = 3000;
        this.inited = false;
    }
    // Methods...
    CommonNotify.prototype.removeNotify = function (notifyData) {
        var _this = this;
        var node = notifyData.node, handler = notifyData.handler;
        // Play animation...
        node.classList.remove('active');
        if (handler) {
            clearTimeout(handler);
            notifyData.handler = undefined;
        }
        setTimeout(function () {
            var _a;
            // ...And remove node (TODO: Check if node still exists in dom tree)...
            try {
                (_a = _this.notifyRoot) === null || _a === void 0 ? void 0 : _a.removeChild(node);
            }
            catch (_e // eslint-disable-line @typescript-eslint/no-unused-vars
            ) {
                // NOOP
            }
        }, 250); // Value of `var(--common-animation-time)`
    };
    /** showNotify
     * @param {'info' | 'error' | 'warn' | 'success'} mode - Message type ('info' is default)
     * @param {string|Error} text - Message content
     */
    CommonNotify.prototype.showNotify = function (mode, text) {
        var _this = this;
        var _a;
        this.ensureInit();
        if (!text) {
            // If only one parameters passed assume it as message with default type
            text = mode;
            mode = 'info';
        }
        var content;
        if (text instanceof Error) {
            // Convert error object to the plain text...
            content = _helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_0__.getErrorText(text);
        }
        else {
            content = String(text);
        }
        // Create node...
        var node = document.createElement('div');
        node.classList.add('notify');
        node.classList.add('notify-' + mode);
        // Add icon...
        var nodeIcon = document.createElement('span');
        nodeIcon.classList.add('icon');
        nodeIcon.classList.add(iconClassNamePrefix);
        nodeIcon.classList.add(icons[mode]);
        node.appendChild(nodeIcon);
        // Add text...
        var nodeText = document.createElement('div');
        nodeText.classList.add('text');
        nodeText.innerHTML = content;
        node.appendChild(nodeText);
        (_a = this.notifyRoot) === null || _a === void 0 ? void 0 : _a.appendChild(node);
        // Play appearing animation...
        window.requestAnimationFrame(function () {
            setTimeout(function () {
                node.classList.add('active');
            }, 10);
        });
        // Remove node after delay...
        var notifyData = { node: node, handler: undefined };
        var removeNotifyHandler = this.removeNotify.bind(this, notifyData);
        notifyData.handler = setTimeout(removeNotifyHandler, this.timeoutDelay);
        // Stop & restore timer on mouse in and out events...
        node.addEventListener('mouseenter', function () {
            // Clear timer...
            clearTimeout(notifyData.handler);
        });
        node.addEventListener('mouseleave', function () {
            // Resume timer...
            notifyData.handler = setTimeout(removeNotifyHandler, _this.timeoutDelay);
        });
        // Click handler...
        node.addEventListener('click', removeNotifyHandler);
    };
    // Some shorthands...
    /** @param {string|Error} text - Message content */
    CommonNotify.prototype.showInfo = function (text) {
        this.showNotify('info', text);
    };
    /** @param {string|Error} text - Message content */
    CommonNotify.prototype.showSuccess = function (text) {
        this.showNotify('success', text);
    };
    /** @param {string|Error} text - Message content */
    CommonNotify.prototype.showWarn = function (text) {
        this.showNotify('warn', text);
    };
    /** @param {string|Error} text - Message content */
    CommonNotify.prototype.showError = function (text) {
        this.showNotify('error', text);
    };
    // Demo...
    CommonNotify.prototype.showDemo = function () {
        // DEBUG: Show sample notifiers...
        this.showInfo('Info');
        this.showSuccess('Success');
        this.showWarn('Warn');
        this.showError('Error');
    };
    // Initialization...
    /** Ensure the modal has initiazlized */
    CommonNotify.prototype.ensureInit = function () {
        this.init();
    };
    CommonNotify.prototype.createDomNode = function () {
        // TODO: To use bootstrap toasts?
        var rootNode = document.body;
        var notifyRoot = document.createElement('div');
        notifyRoot.classList.add('notify-root');
        notifyRoot.setAttribute('id', 'notify-root');
        rootNode.appendChild(notifyRoot);
        this.notifyRoot = notifyRoot;
    };
    /** Initialize nodule. */
    CommonNotify.prototype.init = function () {
        if (!this.inited) {
            this.createDomNode();
            this.inited = true;
        }
    };
    return CommonNotify;
}());
// Create and export singletone
var commonNotify = new CommonNotify();
// commonNotify.init();


/***/ }),

/***/ "./src/assets/checkProjectVersion.ts":
/*!*******************************************!*\
  !*** ./src/assets/checkProjectVersion.ts ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   checkProjectVersion: () => (/* binding */ checkProjectVersion)
/* harmony export */ });
/** Get major and minor versions in form '1.2' from a string 'march-tales v.1.2.20 / 2025.02.20 15:22:00 +0300' */
function getMinorVersionFromProjectInfo(info) {
    if (!info) {
        return undefined;
    }
    try {
        var match = info.match(/^\S+ v\.(\d+\.\d+)/);
        if (match) {
            var v = match[1];
            return v;
        }
    }
    catch (_e // eslint-disable-line @typescript-eslint/no-unused-vars
    ) {
        // NOOP
        return undefined;
    }
}
function checkProjectVersion() {
    var oldInfo = window.localStorage.getItem('projectInfo');
    var newInfo = window.projectInfo;
    if (newInfo && newInfo !== oldInfo) {
        var oldVersion = getMinorVersionFromProjectInfo(oldInfo);
        var newVersion = getMinorVersionFromProjectInfo(newInfo);
        if (newVersion !== oldVersion) {
            // TODO: To clear some stored data etc?
            // eslint-disable-next-line no-console
            console.warn('[checkProjectVersion] Project version has changed', newVersion, '<->', oldVersion, {
                oldInfo: oldInfo,
                newInfo: newInfo,
                oldVersion: oldVersion,
                newVersion: newVersion,
            });
            // debugger; // eslint-disable-line no-debugger
        }
        window.localStorage.setItem('projectInfo', newInfo);
    }
}


/***/ }),

/***/ "./src/assets/constants/acceptedCookiesId.ts":
/*!***************************************************!*\
  !*** ./src/assets/constants/acceptedCookiesId.ts ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   acceptedCookiesId: () => (/* binding */ acceptedCookiesId)
/* harmony export */ });
var acceptedCookiesId = 'cookies';


/***/ }),

/***/ "./src/assets/constants/packDelim.ts":
/*!*******************************************!*\
  !*** ./src/assets/constants/packDelim.ts ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   packDelim: () => (/* binding */ packDelim)
/* harmony export */ });
// Use dashes to save space in cookies (commas are converted to `%2C`-like entities)
var packDelim = '-';


/***/ }),

/***/ "./src/assets/cookies-banner/cookiesBanner.ts":
/*!****************************************************!*\
  !*** ./src/assets/cookies-banner/cookiesBanner.ts ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   initCookiesBanner: () => (/* binding */ initCookiesBanner)
/* harmony export */ });
/* harmony import */ var _constants_acceptedCookiesId__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../constants/acceptedCookiesId */ "./src/assets/constants/acceptedCookiesId.ts");
/* harmony import */ var _helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../helpers/CommonHelpers */ "./src/assets/helpers/CommonHelpers.js");


function updateBannerGeometry(bannerNode) {
    var footerNode = document.querySelector('.template-footer');
    if (!bannerNode || !footerNode) {
        return;
    }
    var bannerHeight = bannerNode.clientHeight;
    footerNode.style.marginBottom = "".concat(bannerHeight, "px");
}
function handleAccept(event) {
    var buttonNode = event.currentTarget;
    var bannerNode = buttonNode.closest('.cookies-banner');
    var value = 'allowed';
    window.localStorage.setItem('cookies', value);
    (0,_helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_1__.setCookie)(_constants_acceptedCookiesId__WEBPACK_IMPORTED_MODULE_0__.acceptedCookiesId, value);
    hideBanner(bannerNode);
}
function handleReject(event) {
    var buttonNode = event.currentTarget;
    var bannerNode = buttonNode.closest('.cookies-banner');
    var value = '';
    window.localStorage.setItem(_constants_acceptedCookiesId__WEBPACK_IMPORTED_MODULE_0__.acceptedCookiesId, value);
    (0,_helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_1__.deleteAllCookies)();
    (0,_helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_1__.setCookie)(_constants_acceptedCookiesId__WEBPACK_IMPORTED_MODULE_0__.acceptedCookiesId, '');
    hideBanner(bannerNode);
}
function initActiveBanner(bannerNode) {
    var _a, _b;
    var eventHandler = updateBannerGeometry.bind(bannerNode);
    window.addEventListener('resize', eventHandler);
    window.addEventListener('orientationchange', eventHandler);
    updateBannerGeometry(bannerNode);
    // Set button handlers...
    (_a = bannerNode
        .querySelector('button#Accept')) === null || _a === void 0 ? void 0 : _a.addEventListener('click', handleAccept);
    (_b = bannerNode
        .querySelector('button#Reject')) === null || _b === void 0 ? void 0 : _b.addEventListener('click', handleReject);
}
function hideBanner(bannerNode) {
    if (bannerNode) {
        bannerNode.remove();
    }
    document.body.classList.add('no-cookies-banner');
}
function initCookiesBanner() {
    var bannerNode = document.querySelector('.cookies-banner');
    if (!bannerNode) {
        return;
    }
    var cookiesBannerStr = window.localStorage.getItem(_constants_acceptedCookiesId__WEBPACK_IMPORTED_MODULE_0__.acceptedCookiesId);
    if (cookiesBannerStr == null) {
        initActiveBanner(bannerNode);
        return;
    }
    hideBanner(bannerNode);
}


/***/ }),

/***/ "./src/assets/entities/ActivePlayerData/ActivePlayerData.ts":
/*!******************************************************************!*\
  !*** ./src/assets/entities/ActivePlayerData/ActivePlayerData.ts ***!
  \******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   loadActivePlayerData: () => (/* binding */ loadActivePlayerData),
/* harmony export */   saveActivePlayerData: () => (/* binding */ saveActivePlayerData)
/* harmony export */ });
var storageActivePlayerDataId = 'ActivePlayerData';
function convertActivePlayerDataFromJsonStr(str) {
    if (!str) {
        return undefined;
    }
    try {
        var raw = JSON.parse(str);
        // const list = str.split(',');
        var 
        // Keep the order!
        id = raw.id, title = raw.title, imageUrl = raw.imageUrl, mediaUrl = raw.mediaUrl, duration = raw.duration, favorite = raw.favorite;
        var data = {
            // Keep the order!
            id: id ? Number(id) : 0,
            title: title ? String(title) : '',
            imageUrl: imageUrl ? String(imageUrl) : '',
            mediaUrl: mediaUrl ? String(mediaUrl) : '',
            duration: duration ? Number(duration) : 0,
            favorite: Boolean(favorite),
        };
        return data;
    }
    catch (err // eslint-disable-line @typescript-eslint/no-unused-vars
    ) {
        // eslint-disable-next-line no-console
        console.warn('[ActivePlayerData:storageActivePlayerDataId] Parse error', {
            str: str,
            err: err,
        });
        return undefined;
    }
}
function convertActivePlayerDataToJsonStr(data) {
    return JSON.stringify(data);
}
function saveActivePlayerData(data) {
    var str = data ? convertActivePlayerDataToJsonStr(data) : '';
    window.localStorage.setItem(storageActivePlayerDataId, str);
}
function loadActivePlayerData() {
    var str = window.localStorage.getItem(storageActivePlayerDataId);
    return convertActivePlayerDataFromJsonStr(str);
}


/***/ }),

/***/ "./src/assets/entities/ActivePlayerData/getActivePlayerDataFromTrackNode.ts":
/*!**********************************************************************************!*\
  !*** ./src/assets/entities/ActivePlayerData/getActivePlayerDataFromTrackNode.ts ***!
  \**********************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getActivePlayerDataFromTrackNode: () => (/* binding */ getActivePlayerDataFromTrackNode)
/* harmony export */ });
function getActivePlayerDataFromTrackNode(trackNode) {
    var dataset = trackNode.dataset;
    var id = Number(dataset.trackId);
    var favorite = Boolean(dataset.favorite);
    // const status = dataset.status;
    var duration = parseFloat((dataset.trackDuration || '0').replace(',', '.'));
    // const position = parseFloat((dataset.position || '0').replace(',', '.'));
    var mediaUrl = dataset.trackMediaUrl || '';
    var imageNode = trackNode.querySelector('img.card-img');
    var imageUrl = (imageNode === null || imageNode === void 0 ? void 0 : imageNode.getAttribute('src')) || '';
    var title = dataset.trackTitle || '';
    var activePlayerData = {
        id: id,
        title: title,
        imageUrl: imageUrl,
        mediaUrl: mediaUrl,
        duration: duration,
        favorite: favorite,
    };
    return activePlayerData;
}


/***/ }),

/***/ "./src/assets/entities/FloatingPlayer/FloatingPlayerCallbacks.ts":
/*!***********************************************************************!*\
  !*** ./src/assets/entities/FloatingPlayer/FloatingPlayerCallbacks.ts ***!
  \***********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FloatingPlayerCallbacks: () => (/* binding */ FloatingPlayerCallbacks)
/* harmony export */ });
// type HandlerId = 'play' | 'stop' | 'time';
var FloatingPlayerCallbacks = /** @class */ (function () {
    function FloatingPlayerCallbacks() {
        this.onPlayStartCallbacks = [];
        this.onPlayStopCallbacks = [];
        this.onUpdateCallbacks = [];
        this.onIncrementCallbacks = [];
        this.onFavoritesCallbacks = [];
        this.onFavoriteCallbacks = [];
        this.onErrorCallbacks = [];
    }
    // handlers: Record<HandlerId, ErrorCallback[]> = {};
    FloatingPlayerCallbacks.prototype.addPlayStartCallback = function (cb) {
        if (cb && !this.onPlayStartCallbacks.includes(cb)) {
            this.onPlayStartCallbacks.push(cb);
        }
    };
    FloatingPlayerCallbacks.prototype.addPlayStopCallback = function (cb) {
        if (cb && !this.onPlayStopCallbacks.includes(cb)) {
            this.onPlayStopCallbacks.push(cb);
        }
    };
    FloatingPlayerCallbacks.prototype.addUpdateCallback = function (cb) {
        if (cb && !this.onUpdateCallbacks.includes(cb)) {
            this.onUpdateCallbacks.push(cb);
        }
    };
    FloatingPlayerCallbacks.prototype.addIncrementCallback = function (cb) {
        if (cb && !this.onIncrementCallbacks.includes(cb)) {
            this.onIncrementCallbacks.push(cb);
        }
    };
    FloatingPlayerCallbacks.prototype.addFavoriteCallback = function (cb) {
        if (cb && !this.onFavoriteCallbacks.includes(cb)) {
            this.onFavoriteCallbacks.push(cb);
        }
    };
    FloatingPlayerCallbacks.prototype.addFavoritesCallback = function (cb) {
        if (cb && !this.onFavoritesCallbacks.includes(cb)) {
            this.onFavoritesCallbacks.push(cb);
        }
    };
    FloatingPlayerCallbacks.prototype.addErrorCallback = function (cb) {
        if (cb && !this.onErrorCallbacks.includes(cb)) {
            this.onErrorCallbacks.push(cb);
        }
    };
    // Invokers
    FloatingPlayerCallbacks.prototype.invokePlayStart = function (data) {
        if (data.activePlayerData) {
            this.onPlayStartCallbacks.forEach(function (cb) {
                cb(data);
            });
        }
    };
    FloatingPlayerCallbacks.prototype.invokePlayStop = function (data) {
        if (data.activePlayerData) {
            this.onPlayStopCallbacks.forEach(function (cb) {
                cb(data);
            });
        }
    };
    FloatingPlayerCallbacks.prototype.invokeUpdate = function (data) {
        if (data.activePlayerData) {
            this.onUpdateCallbacks.forEach(function (cb) {
                cb(data);
            });
        }
    };
    FloatingPlayerCallbacks.prototype.invokeIncrement = function (data) {
        if (data.activePlayerData) {
            this.onIncrementCallbacks.forEach(function (cb) {
                cb(data);
            });
        }
    };
    FloatingPlayerCallbacks.prototype.invokeFavorite = function (data) {
        this.onFavoriteCallbacks.forEach(function (cb) {
            cb(data);
        });
    };
    FloatingPlayerCallbacks.prototype.invokeFavorites = function (data) {
        this.onFavoritesCallbacks.forEach(function (cb) {
            cb(data);
        });
    };
    FloatingPlayerCallbacks.prototype.invokeError = function (error) {
        if (error) {
            this.onErrorCallbacks.forEach(function (cb) {
                cb(error);
            });
        }
    };
    return FloatingPlayerCallbacks;
}());



/***/ }),

/***/ "./src/assets/entities/FloatingPlayer/FloatingPlayerClass.ts":
/*!*******************************************************************!*\
  !*** ./src/assets/entities/FloatingPlayer/FloatingPlayerClass.ts ***!
  \*******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FloatingPlayer: () => (/* binding */ FloatingPlayer)
/* harmony export */ });
/* harmony import */ var _helpers_getJsText__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../helpers/getJsText */ "./src/assets/helpers/getJsText.ts");
/* harmony import */ var _CommonNotify_CommonNotifySingleton__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../CommonNotify/CommonNotifySingleton */ "./src/assets/CommonNotify/CommonNotifySingleton.ts");
/* harmony import */ var _helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../helpers/CommonHelpers */ "./src/assets/helpers/CommonHelpers.js");
/* harmony import */ var _track_blocks_localTrackInfoDb__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../track-blocks/localTrackInfoDb */ "./src/assets/track-blocks/localTrackInfoDb.ts");
/* harmony import */ var _ActivePlayerData_ActivePlayerData__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../ActivePlayerData/ActivePlayerData */ "./src/assets/entities/ActivePlayerData/ActivePlayerData.ts");
/* harmony import */ var _ActivePlayerData_getActivePlayerDataFromTrackNode__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../ActivePlayerData/getActivePlayerDataFromTrackNode */ "./src/assets/entities/ActivePlayerData/getActivePlayerDataFromTrackNode.ts");
/* harmony import */ var _helpers_sendApiRequest__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../helpers/sendApiRequest */ "./src/assets/helpers/sendApiRequest.ts");
/* harmony import */ var _helpers_floatToStr__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../helpers/floatToStr */ "./src/assets/helpers/floatToStr.ts");
/* harmony import */ var _FloatingPlayerState__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./FloatingPlayerState */ "./src/assets/entities/FloatingPlayer/FloatingPlayerState.ts");
/* harmony import */ var _HiddenPlayer__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./HiddenPlayer */ "./src/assets/entities/FloatingPlayer/HiddenPlayer.ts");
/* harmony import */ var _FloatingPlayerCallbacks__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./FloatingPlayerCallbacks */ "./src/assets/entities/FloatingPlayer/FloatingPlayerCallbacks.ts");











// TODO: Update track title on the language change?
var TRUE = 'true';
/** A value of forward/backward seek step */
var seekTimeSec = 1;
var FloatingPlayer = /** @class */ (function () {
    function FloatingPlayer() {
        this.inited = false;
        this.callbacks = new _FloatingPlayerCallbacks__WEBPACK_IMPORTED_MODULE_10__.FloatingPlayerCallbacks();
        this.hiddenPlayer = new _HiddenPlayer__WEBPACK_IMPORTED_MODULE_9__.HiddenPlayer();
        this.state = {};
        this.toggling = {};
        this.seeking = false;
        this.loadActivePlayerData();
        this.loadFloatingPlayerState();
        this.initDomNode();
        this.updateAll();
        // Check if it was recently playing...
        var now = Date.now();
        if (this.activePlayerData) {
            this.ensureAudioLoaded();
            if (this.state.status === 'playing' &&
                this.state.lastTimestamp &&
                this.state.lastTimestamp > now - 5000) {
                // TODO: Then resume playback...
                /* console.log('[FloatingPlayerClass:constructor] Start play', {
                 *   activePlayerData: this.activePlayerData,
                 *   state: this.state,
                 * });
                 */
                // TODO: Care about: `Uncaught (in promise) NotAllowedError: play() failed because the user didn't interact with the document first. https://goo.gl/xX8pDD`
                this.playCurrentPlayer();
            }
            else {
                // Reset the status
                delete this.state.status;
            }
        }
    }
    FloatingPlayer.prototype.requireAudio = function () {
        if (!this.audio) {
            this.audio = this.hiddenPlayer.ensureHiddenPlayerAudio();
            this.audio.addEventListener('canplay', this.handleAudioCanPlay.bind(this));
            this.audio.addEventListener('playing', this.handleAudioPlay.bind(this));
            this.audio.addEventListener('timeupdate', this.handleAudioTimeUpdate.bind(this));
            this.audio.addEventListener('ended', this.handleAudioEnded.bind(this));
            // source.addEventListener('error', this.handleAudioSourceError.bind(this));
        }
        return this.audio;
    };
    FloatingPlayer.prototype.removeAudio = function () {
        this.hiddenPlayer.removeHiddenPlayerAudio();
        this.audio = undefined;
    };
    FloatingPlayer.prototype.hasAudio = function () {
        return !!this.audio;
    };
    FloatingPlayer.prototype.hasAudioSource = function () {
        return this.hiddenPlayer.hasSource();
    };
    FloatingPlayer.prototype.requireDomNode = function () {
        if (!this.domNode) {
            this.domNode = document.querySelector('.floating-player');
            this.hiddenPlayer.setParentDomNode(this.domNode);
        }
        // TODO: Ensure created dom node?
        if (!this.domNode) {
            var error = new Error('No floating player node found');
            // eslint-disable-next-line no-console
            console.error('[FloatingPlayerClass:requireDomNode]', error.message, {
                error: error,
            });
            debugger; // eslint-disable-line no-debugger
            throw error;
        }
        return this.domNode;
    };
    FloatingPlayer.prototype.requireActivePlayerData = function () {
        // TODO: Ensure data?
        if (!this.activePlayerData) {
            var error = new Error('No active player data set');
            // eslint-disable-next-line no-console
            console.error('[FloatingPlayerClass:requireActivePlayerData]', error.message, {
                error: error,
            });
            debugger; // eslint-disable-line no-debugger
            throw error;
        }
        return this.activePlayerData;
    };
    // Sync persistent data...
    FloatingPlayer.prototype.loadActivePlayerData = function () {
        this.activePlayerData = (0,_ActivePlayerData_ActivePlayerData__WEBPACK_IMPORTED_MODULE_4__.loadActivePlayerData)();
    };
    FloatingPlayer.prototype.saveActivePlayerData = function () {
        (0,_ActivePlayerData_ActivePlayerData__WEBPACK_IMPORTED_MODULE_4__.saveActivePlayerData)(this.activePlayerData);
    };
    FloatingPlayer.prototype.loadFloatingPlayerState = function () {
        this.state = (0,_FloatingPlayerState__WEBPACK_IMPORTED_MODULE_8__.loadFloatingPlayerState)();
    };
    FloatingPlayer.prototype.saveFloatingPlayerState = function () {
        (0,_FloatingPlayerState__WEBPACK_IMPORTED_MODULE_8__.saveFloatingPlayerState)(this.state);
    };
    // Dom node...
    FloatingPlayer.prototype.showFloatingPlayer = function () {
        this.state.visible = true;
        this.updateStateInDom();
        this.saveFloatingPlayerState();
    };
    FloatingPlayer.prototype.hideFloatingPlayer = function () {
        this.state.visible = false;
        this.updateStateInDom();
        this.saveFloatingPlayerState();
    };
    // Updaters...
    FloatingPlayer.prototype.updateActivePlayerDataInDom = function () {
        var domNode = this.requireDomNode();
        var activePlayerData = this.requireActivePlayerData();
        var id = activePlayerData.id;
        var titleNode = domNode.querySelector('.title');
        var durationNode = domNode.querySelector('.duration');
        var imageNode = domNode.querySelector('.image');
        var dataset = domNode.dataset;
        requestAnimationFrame(function () {
            titleNode.innerText = activePlayerData.title;
            durationNode.innerText = (0,_helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_2__.formatDuration)(Math.floor(activePlayerData.duration * 1000));
            imageNode.style.backgroundImage = 'url(' + activePlayerData.imageUrl + ')';
            if (activePlayerData.favorite) {
                dataset.favorite = TRUE;
            }
            else {
                delete dataset.favorite;
            }
            var links = domNode.querySelectorAll('.trackLink');
            links.forEach(function (it) {
                it.setAttribute('href', "/tracks/".concat(id, "/"));
            });
        });
    };
    FloatingPlayer.prototype.updateStateInDom = function () {
        var _this = this;
        var domNode = this.requireDomNode();
        var dataset = domNode.dataset;
        requestAnimationFrame(function () {
            if (_this.state.status) {
                dataset.status = _this.state.status;
            }
            else {
                delete dataset.status;
            }
            document.body.classList.toggle('with-player', !!_this.state.visible);
        });
    };
    FloatingPlayer.prototype.updatePositionInDom = function () {
        var _this = this;
        var domNode = this.requireDomNode();
        var seekBarNode = domNode.querySelector('.seekBar');
        var dataset = domNode.dataset;
        requestAnimationFrame(function () {
            dataset.position = (0,_helpers_floatToStr__WEBPACK_IMPORTED_MODULE_7__.floatToStr)(_this.state.position);
            dataset.progress = (0,_helpers_floatToStr__WEBPACK_IMPORTED_MODULE_7__.floatToStr)(_this.state.progress);
            domNode.style.setProperty('--progress', dataset.progress);
            seekBarNode.value = dataset.progress;
        });
    };
    FloatingPlayer.prototype.calculateProgress = function () {
        var activePlayerData = this.requireActivePlayerData();
        var _a = this.state.position, position = _a === void 0 ? 0 : _a;
        var id = activePlayerData.id, duration = activePlayerData.duration;
        if (!duration) {
            var error = new Error("No duration provided for a track: ".concat(id));
            // eslint-disable-next-line no-console
            console.error('[FloatingPlayerClass:calculateProgress]', error.message, {
                error: error,
            });
            debugger; // eslint-disable-line no-debugger
            throw error;
        }
        var ratio = position / duration;
        var progress = Math.min(100, ratio * 100);
        return progress;
    };
    FloatingPlayer.prototype.updateTrackPosition = function () {
        var domNode = this.requireDomNode();
        var timeNode = domNode.querySelector('.time');
        var activePlayerData = this.requireActivePlayerData();
        var _a = this.state.position, position = _a === void 0 ? 0 : _a;
        var id = activePlayerData.id;
        var progress = this.calculateProgress();
        this.state.progress = progress;
        this.updatePositionInDom();
        if (timeNode) {
            requestAnimationFrame(function () {
                timeNode.innerText = (0,_helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_2__.formatDuration)(Math.floor(position * 1000));
            });
        }
        _track_blocks_localTrackInfoDb__WEBPACK_IMPORTED_MODULE_3__.localTrackInfoDb.updatePosition(id, position);
    };
    FloatingPlayer.prototype.updateAll = function () {
        if (this.activePlayerData) {
            this.updateTrackPosition();
        }
        this.updateStateInDom();
        this.updatePositionInDom();
        if (this.activePlayerData) {
            this.updateActivePlayerDataInDom();
        }
    };
    // Audio handlers...
    FloatingPlayer.prototype.handleAudioTimeUpdate = function (ev) {
        if (this.seeking) {
            return;
        }
        var currAudio = this.audio;
        var audio = ev.currentTarget;
        if (audio !== currAudio) {
            return;
        }
        var activePlayerData = this.requireActivePlayerData();
        var currentTime = audio.currentTime;
        /* // DEBUG
         * const source = audio.getElementsByTagName('SOURCE')[0] as HTMLSourceElement;
         * console.log('[FloatingPlayerClass:handleAudioTimeUpdate]', {
         *   currentTime,
         *   readyState,
         *   id: activePlayerData.id,
         *   activePlayerData,
         *   src: source.src,
         *   source,
         *   thisAudio: currAudio === audio,
         *   currAudio,
         *   audio,
         * });
         */
        // TODO: Check loaded status?
        if (this.state.position != currentTime) {
            this.state.position = currentTime;
            this.updateTrackPosition();
            this.saveFloatingPlayerState();
            this.callbacks.invokeUpdate({ floatingPlayerState: this.state, activePlayerData: activePlayerData });
            _track_blocks_localTrackInfoDb__WEBPACK_IMPORTED_MODULE_3__.localTrackInfoDb.updatePosition(activePlayerData.id, currentTime);
        }
    };
    FloatingPlayer.prototype.handleAudioCanPlay = function (_ev) {
        if (!this.state.loaded) {
            this.state.loaded = true;
            delete this.state.error;
        }
    };
    FloatingPlayer.prototype.handleAudioPlay = function (_ev) {
        var activePlayerData = this.requireActivePlayerData();
        this.state.status = 'playing';
        this.updateStateInDom();
        this.saveFloatingPlayerState();
        this.callbacks.invokePlayStart({
            floatingPlayerState: this.state,
            activePlayerData: activePlayerData,
        });
    };
    FloatingPlayer.prototype.handleAudioEnded = function (_ev) {
        var activePlayerData = this.requireActivePlayerData();
        this.incrementPlayedCount();
        this.state.status = 'paused'; // stopped, ready?
        this.updateStateInDom();
        this.saveFloatingPlayerState();
        this.callbacks.invokePlayStop({
            floatingPlayerState: this.state,
            activePlayerData: activePlayerData,
        });
    };
    FloatingPlayer.prototype.handleError = function (err) {
        var errName = err instanceof Error && err.name;
        // eslint-disable-next-line no-console
        console.error('[FloatingPlayerClass:handleError]', {
            err: err,
        });
        if (errName === 'AbortError') {
            // NOTE: Do nothing on abort
            return;
        }
        debugger; // eslint-disable-line no-debugger
        this.state.error = (0,_helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_2__.getErrorText)(err);
        this.updateStateInDom();
        _CommonNotify_CommonNotifySingleton__WEBPACK_IMPORTED_MODULE_1__.commonNotify.showError(err);
        this.callbacks.invokeError(err);
    };
    FloatingPlayer.prototype.handleAudioSourceError = function (ev) {
        var srcElement = ev.currentTarget;
        var src = srcElement.src, type = srcElement.type;
        var errMsg = (0,_helpers_getJsText__WEBPACK_IMPORTED_MODULE_0__.getJsText)('errorLoadingAudioFile') + ' ' + src + (type ? "( ".concat(type, ")") : '');
        var error = new Error(errMsg);
        this.handleError(error);
    };
    /// Active player data
    FloatingPlayer.prototype.getActiveTrackId = function () {
        return this.activePlayerData ? this.activePlayerData.id : undefined;
    };
    // Core handlers...
    FloatingPlayer.prototype.loadAudio = function () {
        var activePlayerData = this.requireActivePlayerData();
        this.state.loaded = false;
        var source = this.hiddenPlayer.createHiddenPlayerSource({ src: activePlayerData.mediaUrl });
        source.addEventListener('error', this.handleAudioSourceError.bind(this));
    };
    FloatingPlayer.prototype.isAudioPlaying = function () {
        var audio = this.audio;
        return (!!audio && audio.currentTime > 0 && !audio.paused && !audio.ended && audio.readyState > 2);
    };
    FloatingPlayer.prototype.isPlaying = function () {
        return this.state.status === 'playing';
    };
    FloatingPlayer.prototype.pauseCurrentPlayer = function () {
        if (this.isAudioPlaying()) {
            var audio = this.requireAudio();
            audio.pause();
        }
        if (this.isPlaying()) {
            this.state.status = 'paused';
            this.updateStateInDom();
            this.saveFloatingPlayerState();
        }
    };
    FloatingPlayer.prototype.playCurrentPlayer = function () {
        var _this = this;
        var audio = this.requireAudio();
        var activePlayerData = this.requireActivePlayerData();
        if (this.isAudioPlaying()) {
            return;
        }
        if (audio.ended ||
            (this.state.position && this.state.position > activePlayerData.duration - 0.1)) {
            // Start from the begining
            this.state.position = 0;
            audio.load();
        }
        this.updateTrackPosition();
        this.callbacks.invokeUpdate({
            floatingPlayerState: this.state,
            activePlayerData: activePlayerData,
        });
        audio.currentTime = this.state.position || 0;
        var result = audio.play();
        result.catch(function (err) {
            if (err.name === 'NotAllowedError') {
                //  play() failed because the user didn't interact with the document first. -> Just cancel
                _this.state.status = undefined;
                _this.updateStateInDom();
            }
            else {
                _this.handleError(err);
            }
        });
    };
    /** Play button click handler */
    FloatingPlayer.prototype.trackPlayHandler = function (_ev) {
        var isPlaying = this.isPlaying();
        if (isPlaying) {
            this.pauseCurrentPlayer();
        }
        else {
            this.playCurrentPlayer();
        }
    };
    // Active player track data...
    FloatingPlayer.prototype.ensureAudioLoaded = function () {
        if (!this.state.loaded || !this.hasAudio() || !this.hasAudioSource) {
            this.loadAudio();
        }
    };
    FloatingPlayer.prototype.setActivePlayerData = function (activePlayerData, position) {
        var _a;
        if (((_a = this.activePlayerData) === null || _a === void 0 ? void 0 : _a.id) !== activePlayerData.id) {
            if (this.activePlayerData && this.isPlaying()) {
                this.pauseCurrentPlayer();
            }
            this.state.loaded = false;
            if (position != null) {
                this.state.position = position;
            }
            this.removeAudio();
            this.activePlayerData = activePlayerData;
        }
        this.saveActivePlayerData();
        this.updateActivePlayerDataInDom();
        this.ensureAudioLoaded();
    };
    FloatingPlayer.prototype.setActiveTrack = function (trackNode, position) {
        var activePlayerData = (0,_ActivePlayerData_getActivePlayerDataFromTrackNode__WEBPACK_IMPORTED_MODULE_5__.getActivePlayerDataFromTrackNode)(trackNode);
        this.setActivePlayerData(activePlayerData, position);
    };
    FloatingPlayer.prototype.clearActiveData = function () {
        this.activePlayerData = undefined;
        this.hideFloatingPlayer();
        this.removeAudio();
    };
    // Update related data
    FloatingPlayer.prototype.sendIncrementPlayedCount = function (id) {
        var url = "/api/v1/tracks/".concat(id, "/increment-played-count/");
        return (0,_helpers_sendApiRequest__WEBPACK_IMPORTED_MODULE_6__.sendApiRequest)(url, 'POST');
    };
    FloatingPlayer.prototype.incrementPlayedCount = function () {
        var _this = this;
        var activePlayerData = this.requireActivePlayerData();
        if (this.incrementing) {
            return;
        }
        this.incrementing = true;
        return this.sendIncrementPlayedCount(activePlayerData.id)
            .then(function (_a) {
            var played_count = _a.played_count;
            if (played_count != null) {
                // Re-update local data with server data...
                _this.callbacks.invokeIncrement({ count: played_count, activePlayerData: activePlayerData });
            }
            // TODO: Update other instances of this track on the page (eg, in player, or in other track listings)?
        })
            .catch(function (err) {
            // eslint-disable-next-line no-console
            console.error('[FloatingPlayerClass:incrementPlayedCount:sendIncrementPlayedCount] error', {
                err: err,
            });
            debugger; // eslint-disable-line no-debugger
            _CommonNotify_CommonNotifySingleton__WEBPACK_IMPORTED_MODULE_1__.commonNotify.showError(err);
            // Increment locally (?)
            _this.callbacks.invokeIncrement({ activePlayerData: activePlayerData });
            throw err;
        })
            .finally(function () {
            _this.incrementing = false;
        });
    };
    FloatingPlayer.prototype.sendToggleFavoriteRequest = function (id, value) {
        var url = "/api/v1/tracks/".concat(id, "/toggle-favorite/");
        return (0,_helpers_sendApiRequest__WEBPACK_IMPORTED_MODULE_6__.sendApiRequest)(url, 'POST', { value: value });
    };
    FloatingPlayer.prototype.toggleFavorite = function () {
        var activePlayerData = this.requireActivePlayerData();
        var id = activePlayerData.id;
        this.toggleFavoriteById(id);
    };
    FloatingPlayer.prototype.toggleFavoriteById = function (id) {
        var _this = this;
        if (this.toggling[id]) {
            return;
        }
        var activePlayerData = this.activePlayerData;
        var isCurrent = id === (activePlayerData === null || activePlayerData === void 0 ? void 0 : activePlayerData.id);
        var trackInfo = _track_blocks_localTrackInfoDb__WEBPACK_IMPORTED_MODULE_3__.localTrackInfoDb.getById(id);
        var nextFavorite = !(trackInfo === null || trackInfo === void 0 ? void 0 : trackInfo.favorite);
        /* console.log('[FloatingPlayerClass:toggleFavoriteById]', {
         *   activePlayerData,
         *   isCurrent,
         *   trackInfo,
         *   nextFavorite,
         * });
         */
        _track_blocks_localTrackInfoDb__WEBPACK_IMPORTED_MODULE_3__.localTrackInfoDb.updateFavorite(id, nextFavorite);
        if (isCurrent) {
            activePlayerData.favorite = nextFavorite;
            this.updateActivePlayerDataInDom();
            this.saveActivePlayerData();
        }
        this.callbacks.invokeFavorite({ id: id, favorite: nextFavorite });
        if (window.isAuthenticated) {
            this.toggling[id] = true;
            this.sendToggleFavoriteRequest(id, nextFavorite)
                .then(function (results) {
                var favorite_track_ids = results.favorite_track_ids;
                _track_blocks_localTrackInfoDb__WEBPACK_IMPORTED_MODULE_3__.localTrackInfoDb.updateFavoritesByTrackIds(favorite_track_ids);
                _this.callbacks.invokeFavorites({
                    favorites: favorite_track_ids,
                });
                var msgId = nextFavorite ? 'trackAddedToFavorites' : 'trackRemovedFromFavorites';
                _CommonNotify_CommonNotifySingleton__WEBPACK_IMPORTED_MODULE_1__.commonNotify.showSuccess((0,_helpers_getJsText__WEBPACK_IMPORTED_MODULE_0__.getJsText)(msgId));
            })
                .catch(function (err) {
                // eslint-disable-next-line no-console
                console.error('[FloatingPlayerClass:toggleFavoriteById] error', {
                    err: err,
                });
                debugger; // eslint-disable-line no-debugger
                _CommonNotify_CommonNotifySingleton__WEBPACK_IMPORTED_MODULE_1__.commonNotify.showError(err);
            })
                .finally(function () {
                _this.toggling[id] = false;
            });
        }
    };
    FloatingPlayer.prototype.seekPosition = function (position) {
        var _this = this;
        this.seeking = true;
        var audio = this.requireAudio();
        audio.currentTime = position || 0;
        this.state.position = position;
        this.updateTrackPosition();
        this.saveFloatingPlayerState();
        var activePlayerData = this.requireActivePlayerData();
        this.callbacks.invokeUpdate({ floatingPlayerState: this.state, activePlayerData: activePlayerData });
        setTimeout(function () {
            _this.seeking = false;
        }, 150);
    };
    FloatingPlayer.prototype.seekRewind = function () {
        var position = Math.max(0, (this.state.position || 0) - seekTimeSec);
        this.seekPosition(position);
    };
    FloatingPlayer.prototype.seekForward = function () {
        var activePlayerData = this.requireActivePlayerData();
        var duration = activePlayerData.duration;
        var position = Math.min(duration, (this.state.position || 0) + seekTimeSec);
        this.seekPosition(position);
    };
    FloatingPlayer.prototype.seekBarHandle = function (ev) {
        var activePlayerData = this.requireActivePlayerData();
        var duration = activePlayerData.duration;
        if (!duration) {
            return;
        }
        var node = ev.currentTarget;
        var value = Number(node.value);
        var position = (value * duration) / 100;
        this.seekPosition(position);
        if (!this.isPlaying()) {
            this.playCurrentPlayer();
        }
    };
    // Initilization...
    FloatingPlayer.prototype.initDomNode = function () {
        var _this = this;
        var domNode = this.requireDomNode();
        var seekBarNode = domNode.querySelector('.seekBar');
        if (seekBarNode) {
            seekBarNode.addEventListener('input', this.seekBarHandle.bind(this));
        }
        var hideButton = domNode.querySelector('.track-control-hide');
        if (hideButton) {
            hideButton.addEventListener('click', this.hideFloatingPlayer.bind(this));
        }
        var controls = domNode.querySelectorAll('.track-control');
        controls.forEach(function (node) {
            var dataset = node.dataset;
            var inited = dataset.inited, controlId = dataset.controlId;
            if (inited) {
                return;
            }
            if (controlId === 'rewind') {
                node.addEventListener('click', _this.seekRewind.bind(_this));
            }
            if (controlId === 'forward') {
                node.addEventListener('click', _this.seekForward.bind(_this));
            }
            if (controlId === 'toggleFavorite') {
                node.addEventListener('click', _this.toggleFavorite.bind(_this));
            }
            if (controlId === 'play') {
                node.addEventListener('click', _this.trackPlayHandler.bind(_this));
            }
            dataset.inited = TRUE;
        });
        this.inited = true;
    };
    return FloatingPlayer;
}());



/***/ }),

/***/ "./src/assets/entities/FloatingPlayer/FloatingPlayerState.ts":
/*!*******************************************************************!*\
  !*** ./src/assets/entities/FloatingPlayer/FloatingPlayerState.ts ***!
  \*******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   loadFloatingPlayerState: () => (/* binding */ loadFloatingPlayerState),
/* harmony export */   saveFloatingPlayerState: () => (/* binding */ saveFloatingPlayerState)
/* harmony export */ });
/* harmony import */ var _helpers_floatToStr__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../helpers/floatToStr */ "./src/assets/helpers/floatToStr.ts");
var __assign = (undefined && undefined.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};

var storageFloatingPlayerStateId = 'FloatingPlayerState';
function convertFloatingPlayerStateFromJsonStr(str) {
    if (!str) {
        return {};
    }
    try {
        var list = str.split(',');
        var 
        // Keep the order!
        lastTimestamp = list[0], visible = list[1], status_1 = list[2], position = list[3], progress = list[4];
        var data = {
            // Keep the order!
            lastTimestamp: lastTimestamp ? Number(lastTimestamp) * 1000 : undefined, // Timestamp
            visible: visible ? Boolean(visible) : undefined,
            status: status_1 ? String(status_1) : undefined,
            position: position ? Number(position) : undefined,
            progress: progress ? Number(progress) : undefined,
        };
        return data;
    }
    catch (err // eslint-disable-line @typescript-eslint/no-unused-vars
    ) {
        // eslint-disable-next-line no-console
        console.warn('[FloatingPlayerState:convertFloatingPlayerStateFromJsonStr] Parse error', {
            str: str,
            err: err,
        });
        return {};
    }
}
function convertFloatingPlayerStateToJsonStr(data) {
    var 
    // Keep the order!
    lastTimestamp = data.lastTimestamp, visible = data.visible, status = data.status, position = data.position, progress = data.progress;
    var list = [
        // Keep the order!
        lastTimestamp ? Math.round(lastTimestamp / 1000) : undefined, // Timestamp
        visible ? Number(visible) : undefined, // Boolean
        status ? status : undefined,
        position ? (0,_helpers_floatToStr__WEBPACK_IMPORTED_MODULE_0__.floatToStr)(position) : undefined,
        progress ? (0,_helpers_floatToStr__WEBPACK_IMPORTED_MODULE_0__.floatToStr)(progress) : undefined,
    ];
    var str = list.join(',').replace(/,+$/, '');
    return str;
}
function saveFloatingPlayerState(data) {
    var saveData = __assign(__assign({}, data), { lastTimestamp: Date.now() });
    var str = convertFloatingPlayerStateToJsonStr(saveData);
    window.localStorage.setItem(storageFloatingPlayerStateId, str);
}
function loadFloatingPlayerState() {
    var str = window.localStorage.getItem(storageFloatingPlayerStateId);
    return convertFloatingPlayerStateFromJsonStr(str);
}


/***/ }),

/***/ "./src/assets/entities/FloatingPlayer/HiddenPlayer.ts":
/*!************************************************************!*\
  !*** ./src/assets/entities/FloatingPlayer/HiddenPlayer.ts ***!
  \************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   HiddenPlayer: () => (/* binding */ HiddenPlayer)
/* harmony export */ });
var HiddenPlayer = /** @class */ (function () {
    function HiddenPlayer() {
    }
    HiddenPlayer.prototype.setParentDomNode = function (parentDomNode) {
        this.parentDomNode = parentDomNode;
    };
    HiddenPlayer.prototype.requireParentDomNode = function () {
        return this.parentDomNode || document.body;
    };
    HiddenPlayer.prototype.ensureHiddenPlayer = function ( /* opts: THiddenPlayerOptions = {} */) {
        if (!this.hiddenPlayerNode) {
            this.hiddenPlayerNode = document.createElement('div');
            this.hiddenPlayerNode.classList.add('hidden-player');
            var audio = document.createElement('audio');
            // audio.addEventListener('loadeddata', this.hiddenPlayerCanPlay);
            this.hiddenPlayerNode.appendChild(audio);
            var parentDomNode = this.requireParentDomNode();
            parentDomNode.appendChild(this.hiddenPlayerNode);
        }
        return this.hiddenPlayerNode;
    };
    HiddenPlayer.prototype.hasAudio = function () {
        return !!this.audioNode;
    };
    HiddenPlayer.prototype.hasSource = function () {
        return !!this.sourceNode;
    };
    HiddenPlayer.prototype.ensureHiddenPlayerAudio = function () {
        if (!this.audioNode) {
            var parentDomNode = this.requireParentDomNode();
            this.audioNode = document.createElement('audio');
            this.audioNode.classList.add('hidden-player');
            this.audioNode.setAttribute('preload', 'auto');
            // audio.addEventListener('loadeddata', this.hiddenPlayerCanPlay);
            parentDomNode.appendChild(this.audioNode);
        }
        return this.audioNode;
    };
    HiddenPlayer.prototype.createHiddenPlayerSource = function (opts) {
        if (opts === void 0) { opts = {}; }
        this.removeHiddenPlayerSource();
        var audio = this.ensureHiddenPlayerAudio();
        this.sourceNode = document.createElement('source');
        this.sourceNode.setAttribute('type', opts.type || 'audio/mpeg');
        if (opts.src) {
            this.sourceNode.setAttribute('src', opts.src);
        }
        // @see https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/loadeddata_event
        // audio.addEventListener('canplay', this.handleCanPlay.bind(this));
        // audio.addEventListener('playing', this.handlePlay.bind(this));
        // audio.addEventListener('timeupdate', this.handleTimeUpdate.bind(this));
        // audio.addEventListener('ended', this.handleEnded.bind(this));
        // this.sourceNode.addEventListener('error', this.handleError.bind(this));
        audio.appendChild(this.sourceNode);
        return this.sourceNode;
    };
    HiddenPlayer.prototype.removeHiddenPlayerAudio = function () {
        if (this.audioNode) {
            this.audioNode.pause();
            this.audioNode.remove();
            this.audioNode = undefined;
            this.sourceNode = undefined;
        }
    };
    HiddenPlayer.prototype.removeHiddenPlayerSource = function () {
        var audio = this.ensureHiddenPlayerAudio();
        var prevSources = Array.from(audio.getElementsByTagName('source'));
        for (var _i = 0, prevSources_1 = prevSources; _i < prevSources_1.length; _i++) {
            var node = prevSources_1[_i];
            node.remove();
        }
        this.sourceNode = undefined;
    };
    return HiddenPlayer;
}());



/***/ }),

/***/ "./src/assets/entities/FloatingPlayer/floatingPlayer.ts":
/*!**************************************************************!*\
  !*** ./src/assets/entities/FloatingPlayer/floatingPlayer.ts ***!
  \**************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   floatingPlayer: () => (/* binding */ floatingPlayer),
/* harmony export */   initFloatingPlayer: () => (/* binding */ initFloatingPlayer)
/* harmony export */ });
/* harmony import */ var _FloatingPlayerClass__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./FloatingPlayerClass */ "./src/assets/entities/FloatingPlayer/FloatingPlayerClass.ts");

// Singleton
var floatingPlayer = new _FloatingPlayerClass__WEBPACK_IMPORTED_MODULE_0__.FloatingPlayer();
function initFloatingPlayer() {
    // console.log('[floatingPlayer:initFloatingPlayer]');
}


/***/ }),

/***/ "./src/assets/helpers/floatToStr.ts":
/*!******************************************!*\
  !*** ./src/assets/helpers/floatToStr.ts ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   floatToStr: () => (/* binding */ floatToStr)
/* harmony export */ });
function floatToStr(num) {
    if (!num) {
        return '0';
    }
    if (typeof num === 'string') {
        if (isNaN(num)) {
            return '0';
        }
        num = Number(num);
    }
    return num
        .toFixed(3)
        .replace(/(\.\d+)0+$/, '$1')
        .replace(/\.0+$/, '');
}


/***/ }),

/***/ "./src/assets/helpers/getJsText.ts":
/*!*****************************************!*\
  !*** ./src/assets/helpers/getJsText.ts ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getJsText: () => (/* binding */ getJsText)
/* harmony export */ });
/* harmony import */ var _helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../helpers/CommonHelpers */ "./src/assets/helpers/CommonHelpers.js");

function getJsText(id) {
    var textNode = document.body.querySelector('#js-texts #' + id);
    if (!textNode) {
        // eslint-disable-next-line no-console
        console.warn('[getJsText] Can not find js text node for id:', id);
    }
    var text = (textNode === null || textNode === void 0 ? void 0 : textNode.innerHTML) || id;
    return (0,_helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_0__.quoteHtmlAttr)(text).trim();
}


/***/ }),

/***/ "./src/assets/helpers/sendApiRequest.ts":
/*!**********************************************!*\
  !*** ./src/assets/helpers/sendApiRequest.ts ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   sendApiRequest: () => (/* binding */ sendApiRequest)
/* harmony export */ });
/* harmony import */ var _helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../helpers/CommonHelpers */ "./src/assets/helpers/CommonHelpers.js");
/* harmony import */ var _getJsText__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./getJsText */ "./src/assets/helpers/getJsText.ts");
var __awaiter = (undefined && undefined.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (undefined && undefined.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};



function sendApiRequest(url, method, requestData) {
    var _this = this;
    if (method === void 0) { method = 'GET'; }
    var csrftoken = (0,_helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_0__.getCookie)('csrftoken');
    var headers = {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken || '',
        // Credentials: 'include',
        // Cookie: csrftoken && `csrftoken=${csrftoken}`,
        // 'X-Session-Token': sessionId, // X-Session-Token
        // 'Accept-Language': 'ru', // django_language=ru; content-language: ru;
    };
    return fetch(url, {
        method: method,
        headers: headers,
        credentials: 'include',
        body: requestData ? JSON.stringify(requestData) : null,
    })
        .then(function (res) { return __awaiter(_this, void 0, void 0, function () {
        var ok, status, statusText, data, _e_1, errMsg;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    ok = res.ok, status = res.status, statusText = res.statusText;
                    data = undefined;
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, res.json()];
                case 2:
                    data = _a.sent();
                    return [3 /*break*/, 4];
                case 3:
                    _e_1 = _a.sent();
                    return [3 /*break*/, 4];
                case 4:
                    if (!ok || status !== 200) {
                        errMsg = [(0,_getJsText__WEBPACK_IMPORTED_MODULE_1__.getJsText)('fetchError') + ' ' + status, (data === null || data === void 0 ? void 0 : data.detail) || statusText]
                            .filter(Boolean)
                            .join(': ');
                        // eslint-disable-next-line no-console
                        console.error('[sendApiRequest]', errMsg, {
                            ok: ok,
                            data: data,
                            statusText: statusText,
                            status: status,
                            res: res,
                            url: url,
                            requestData: requestData,
                            method: method,
                            headers: headers,
                        });
                        debugger; // eslint-disable-line no-debugger
                        throw new Error(errMsg);
                    }
                    return [2 /*return*/, data];
            }
        });
    }); })
        .catch(function (err) {
        var errMsg = [(0,_getJsText__WEBPACK_IMPORTED_MODULE_1__.getJsText)('failedApiRequest'), _helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_0__.getErrorText(err)]
            .filter(Boolean)
            .join(': ');
        // eslint-disable-next-line no-console
        console.error('[sendApiRequest]', errMsg, {
            err: err,
            url: url,
            requestData: requestData,
            method: method,
            headers: headers,
        });
        debugger; // eslint-disable-line no-debugger
        throw new Error(errMsg);
    });
}


/***/ }),

/***/ "./src/assets/processTextContent.ts":
/*!******************************************!*\
  !*** ./src/assets/processTextContent.ts ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   processTextContent: () => (/* binding */ processTextContent)
/* harmony export */ });
function processLink(node) {
    if (!node.classList.contains('external')) {
        node.classList.add('external');
        node.setAttribute('target', '_blank');
        var nodeIcon = document.createElement('span');
        nodeIcon.classList.add('icon', 'icon-external', 'bi', 'bi-box-arrow-up-right');
        node.appendChild(nodeIcon);
    }
}
function processTextBlock(node) {
    // Find external links...
    var linkNodes = node.querySelectorAll('a[href^="https://"]');
    linkNodes.forEach(processLink);
}
function processTextContent() {
    var textNodes = document.querySelectorAll('.text-content');
    textNodes.forEach(processTextBlock);
}


/***/ }),

/***/ "./src/assets/track-blocks/TrackInfo.ts":
/*!**********************************************!*\
  !*** ./src/assets/track-blocks/TrackInfo.ts ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   trackInfoFromJsonStr: () => (/* binding */ trackInfoFromJsonStr),
/* harmony export */   trackInfoToJsonStr: () => (/* binding */ trackInfoToJsonStr)
/* harmony export */ });
/* harmony import */ var _helpers_floatToStr__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../helpers/floatToStr */ "./src/assets/helpers/floatToStr.ts");
/* harmony import */ var _constants_packDelim__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../constants/packDelim */ "./src/assets/constants/packDelim.ts");


var finalPackDelimReg = new RegExp(_constants_packDelim__WEBPACK_IMPORTED_MODULE_1__.packDelim + '+$');
function trackInfoFromJsonStr(str) {
    if (!str) {
        return undefined;
    }
    try {
        var list = str.split(_constants_packDelim__WEBPACK_IMPORTED_MODULE_1__.packDelim);
        var 
        // Keep the order!
        id = list[0], favorite = list[1], playedCount = list[2], position = list[3], lastUpdated = list[4], // Timestamp
        lastPlayed = list[5];
        var data = {
            // Keep the order!
            id: id ? Number(id) : 0,
            favorite: Boolean(favorite),
            playedCount: playedCount ? Number(playedCount) : 0,
            position: position ? Number(position) : 0,
            lastUpdated: lastUpdated ? Number(lastUpdated) * 1000 : 0, // Timestamp
            lastPlayed: lastPlayed ? Number(lastPlayed) * 1000 : 0, // Timestamp
        };
        return data;
    }
    catch (err // eslint-disable-line @typescript-eslint/no-unused-vars
    ) {
        // eslint-disable-next-line no-console
        console.warn('[TrackInfo:trackInfoFromJsonStr] Parse error', {
            str: str,
            err: err,
        });
        return undefined;
    }
}
function trackInfoToJsonStr(trackInfo) {
    var 
    // Keep the order!
    id = trackInfo.id, favorite = trackInfo.favorite, playedCount = trackInfo.playedCount, position = trackInfo.position, lastUpdated = trackInfo.lastUpdated, lastPlayed = trackInfo.lastPlayed;
    var list = [
        // Keep the order!
        id ? Number(id) : undefined,
        favorite ? Number(favorite) : undefined,
        playedCount ? Number(playedCount) : undefined,
        position ? (0,_helpers_floatToStr__WEBPACK_IMPORTED_MODULE_0__.floatToStr)(position) : undefined, // Use fixed decimal presentation for floats
        lastUpdated ? Math.round(lastUpdated / 1000) : undefined, // Timestamp
        lastPlayed ? Math.round(lastPlayed / 1000) : undefined, // Timestamp
    ];
    return list.join(_constants_packDelim__WEBPACK_IMPORTED_MODULE_1__.packDelim).replace(finalPackDelimReg, '');
}


/***/ }),

/***/ "./src/assets/track-blocks/localTrackInfoDb.ts":
/*!*****************************************************!*\
  !*** ./src/assets/track-blocks/localTrackInfoDb.ts ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   localTrackInfoDb: () => (/* binding */ localTrackInfoDb)
/* harmony export */ });
/* harmony import */ var _TrackInfo__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./TrackInfo */ "./src/assets/track-blocks/TrackInfo.ts");
/* harmony import */ var _helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../helpers/CommonHelpers */ "./src/assets/helpers/CommonHelpers.js");
/* harmony import */ var _constants_packDelim__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../constants/packDelim */ "./src/assets/constants/packDelim.ts");
/* harmony import */ var _constants_acceptedCookiesId__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../constants/acceptedCookiesId */ "./src/assets/constants/acceptedCookiesId.ts");




/* TODO: Use `new CustomEvent` to broadcast events */
var LocalTrackInfoDb = /** @class */ (function () {
    function LocalTrackInfoDb() {
    }
    // End-user api
    LocalTrackInfoDb.prototype.updatePlayedCount = function (id, playedCount, now) {
        try {
            var _now = now || Date.now();
            var trackInfo = this.getOrCreate(id);
            if (playedCount == undefined || isNaN(playedCount)) {
                trackInfo.playedCount = trackInfo.playedCount ? trackInfo.playedCount + 1 : 1;
            }
            else {
                trackInfo.playedCount = playedCount;
            }
            trackInfo.lastPlayed = _now;
            trackInfo.lastUpdated = _now;
            this.insert(trackInfo);
            // this.updateEvents.broadcast(TracksInfoDbUpdate(trackInfo));
            return trackInfo;
        }
        catch (err) {
            // eslint-disable-next-line no-console
            console.error('[LocalTrackInfoDb:incrementPlayedCount]', err.message, {
                err: err,
                id: id,
            });
            debugger; // eslint-disable-line no-debugger
            throw err;
        }
    };
    LocalTrackInfoDb.prototype.updatePosition = function (id, position, now) {
        try {
            var _now = now || Date.now();
            var trackInfo = this.getOrCreate(id);
            trackInfo.position = position;
            trackInfo.lastPlayed = _now; // ???
            trackInfo.lastUpdated = _now;
            this.insert(trackInfo);
            // this.updateEvents.broadcast(TracksInfoDbUpdate(trackInfo));
            return trackInfo;
        }
        catch (err) {
            // eslint-disable-next-line no-console
            console.error('[LocalTrackInfoDb:updatePosition]', err.message, {
                err: err,
                id: id,
            });
            debugger; // eslint-disable-line no-debugger
            throw err;
        }
    };
    LocalTrackInfoDb.prototype.updateFavorite = function (id, favorite, now) {
        try {
            var _now = now || Date.now();
            var trackInfo = this.getOrCreate(id);
            trackInfo.favorite = favorite;
            trackInfo.lastUpdated = _now;
            this.insert(trackInfo);
            this._toggleInFavoritesIndex(id, favorite);
            // this.updateEvents.broadcast(TracksInfoDbUpdate(trackInfo));
            return trackInfo;
        }
        catch (err) {
            // eslint-disable-next-line no-console
            console.error('[LocalTrackInfoDb:setFavorite]', err.message, {
                err: err,
                id: id,
            });
            debugger; // eslint-disable-line no-debugger
            throw err;
        }
    };
    LocalTrackInfoDb.prototype.updateFavoritesByTrackIds = function (ids, now) {
        var _this = this;
        var _now = now || Date.now();
        var index = this._getIndex();
        index.forEach(function (id) {
            var isFavorite = ids.includes(id);
            var trackInfo = _this.getOrCreate(id);
            if (trackInfo.favorite !== isFavorite) {
                trackInfo.favorite = isFavorite;
                trackInfo.lastUpdated = _now;
                _this.insert(trackInfo);
            }
        });
        this._setFavoritesIndex(ids);
    };
    LocalTrackInfoDb.prototype.save = function (trackInfo, now) {
        try {
            var _now = now || Date.now();
            trackInfo.lastPlayed = _now; // ???
            trackInfo.lastUpdated = _now;
            this.insert(trackInfo);
            // this.updateEvents.broadcast(TracksInfoDbUpdate(trackInfo));
            // const testTrackInfo = await this.getById(id);
            return trackInfo;
        }
        catch (err) {
            // eslint-disable-next-line no-console
            console.error('[LocalTrackInfoDb:save]', err.message, {
                err: err,
                trackInfo: trackInfo,
            });
            debugger; // eslint-disable-line no-debugger
            throw err;
        }
    };
    // Low-level api
    LocalTrackInfoDb.prototype.createNewRecord = function (id) {
        var now = Date.now();
        var trackInfo = {
            id: id, // track.id
            favorite: false,
            playedCount: 0, // track.played_count (but only for current user!).
            position: 0, // position
            lastUpdated: now, // DateTime.now()
            lastPlayed: 0, // DateTime.now()
        };
        return trackInfo;
    };
    LocalTrackInfoDb.prototype.getOrCreate = function (id) {
        return this.getById(id) || this.createNewRecord(id);
    };
    /// Create or update the record. (Returns inserted/updated record id.)
    LocalTrackInfoDb.prototype.insert = function (trackInfo) {
        var id = trackInfo.id;
        var str = (0,_TrackInfo__WEBPACK_IMPORTED_MODULE_0__.trackInfoToJsonStr)(trackInfo);
        window.localStorage.setItem('ti-' + id, str);
        this._addToIndex(id);
    };
    LocalTrackInfoDb.prototype.getFavorites = function () {
        return this.getAll().filter(function (it) { return it.favorite; });
    };
    LocalTrackInfoDb.prototype.getById = function (id) {
        var str = window.localStorage.getItem('ti-' + id);
        if (!str) {
            return undefined;
        }
        return (0,_TrackInfo__WEBPACK_IMPORTED_MODULE_0__.trackInfoFromJsonStr)(str);
    };
    LocalTrackInfoDb.prototype._getFavoritesIndex = function () {
        try {
            var str = window.localStorage.getItem('favorites');
            if (!str) {
                return [];
            }
            var list = str
                .split(_constants_packDelim__WEBPACK_IMPORTED_MODULE_2__.packDelim)
                .map(Number)
                .filter(function (n) { return !isNaN(n); });
            return list;
        }
        catch (_ // eslint-disable-line @typescript-eslint/no-unused-vars
        ) {
            return [];
        }
    };
    LocalTrackInfoDb.prototype._setFavoritesIndex = function (favoritesIndex) {
        var list = favoritesIndex.filter(function (n) { return !isNaN(n); }).filter(Boolean);
        var str = list.join(_constants_packDelim__WEBPACK_IMPORTED_MODULE_2__.packDelim);
        window.localStorage.setItem('favorites', str);
        // Update cookie value and document status
        var favoritesCount = list.length;
        var hasFavorites = !!favoritesCount;
        document.body.classList.toggle('has-favorites', hasFavorites);
        // Update count texts
        document.querySelectorAll('.favorites-count').forEach(function (node) {
            node.innerText = String(favoritesCount);
        });
        // Update cookie
        if (window.localStorage.getItem(_constants_acceptedCookiesId__WEBPACK_IMPORTED_MODULE_3__.acceptedCookiesId)) {
            (0,_helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_1__.setCookie)('favorites', str);
        }
    };
    LocalTrackInfoDb.prototype._addToFavoritesIndex = function (id) {
        var favoritesIndex = this._getFavoritesIndex();
        if (!favoritesIndex.includes(id)) {
            favoritesIndex.push(id);
            this._setFavoritesIndex(favoritesIndex);
        }
    };
    LocalTrackInfoDb.prototype._removeFromFavoritesIndex = function (id) {
        var favoritesIndex = this._getFavoritesIndex();
        if (favoritesIndex.includes(id)) {
            this._setFavoritesIndex(favoritesIndex.filter(function (checkId) { return id !== checkId; }));
        }
    };
    LocalTrackInfoDb.prototype._toggleInFavoritesIndex = function (id, value) {
        if (value) {
            this._addToFavoritesIndex(id);
        }
        else {
            this._removeFromFavoritesIndex(id);
        }
    };
    LocalTrackInfoDb.prototype._getIndex = function () {
        try {
            var str = window.localStorage.getItem('ti-index');
            return (str ? str.split(_constants_packDelim__WEBPACK_IMPORTED_MODULE_2__.packDelim).map(function (v) { return (v ? Number(v) : 0); }) : []);
        }
        catch (_ // eslint-disable-line @typescript-eslint/no-unused-vars
        ) {
            return [];
        }
    };
    LocalTrackInfoDb.prototype._setIndex = function (index) {
        window.localStorage.setItem('ti-index', index.join(_constants_packDelim__WEBPACK_IMPORTED_MODULE_2__.packDelim));
    };
    LocalTrackInfoDb.prototype._addToIndex = function (id) {
        var index = this._getIndex();
        if (!index.includes(id)) {
            index.push(id);
            this._setIndex(index);
        }
    };
    LocalTrackInfoDb.prototype._removeFromIndex = function (id) {
        var index = this._getIndex();
        if (index.includes(id)) {
            this._setIndex(index.filter(function (checkId) { return id !== checkId; }));
        }
    };
    LocalTrackInfoDb.prototype._toggleInIndex = function (id, value) {
        if (value) {
            this._addToIndex(id);
        }
        else {
            this._removeFromIndex(id);
        }
    };
    LocalTrackInfoDb.prototype.getAll = function () {
        var _this = this;
        var index = this._getIndex();
        var list = index
            .map(function (id) {
            return _this.getById(id);
        })
            .filter(Boolean);
        return list;
    };
    LocalTrackInfoDb.prototype.delete = function (id) {
        window.localStorage.removeItem('ti-' + id);
        this._removeFromIndex(id);
    };
    LocalTrackInfoDb.prototype.clearAll = function () {
        var index = this._getIndex();
        index.forEach(function (id) {
            window.localStorage.removeItem('ti-' + id);
        });
        this._setIndex([]);
    };
    return LocalTrackInfoDb;
}());
// Create a singleton
var localTrackInfoDb = new LocalTrackInfoDb();


/***/ }),

/***/ "./src/assets/track-blocks/tracksPlayer.ts":
/*!*************************************************!*\
  !*** ./src/assets/track-blocks/tracksPlayer.ts ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   initTracksPlayerWrapper: () => (/* binding */ initTracksPlayerWrapper)
/* harmony export */ });
/* harmony import */ var _helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../helpers/CommonHelpers */ "./src/assets/helpers/CommonHelpers.js");
/* harmony import */ var _localTrackInfoDb__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./localTrackInfoDb */ "./src/assets/track-blocks/localTrackInfoDb.ts");
/* harmony import */ var _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../entities/FloatingPlayer/floatingPlayer */ "./src/assets/entities/FloatingPlayer/floatingPlayer.ts");
/* harmony import */ var _helpers_floatToStr__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../helpers/floatToStr */ "./src/assets/helpers/floatToStr.ts");




var allPlayers;
var currentTrackPlayer = undefined;
// Values for dataset statuses
var TRUE = 'true';
function calculateAndUpdateTrackPosition(trackNode, position, _isCurrent) {
    var timeNode = trackNode.querySelector('.time');
    var dataset = trackNode.dataset;
    var trackId = dataset.trackId, trackDuration = dataset.trackDuration;
    var timeMs = Math.floor(position * 1000);
    var timeFormatted = (0,_helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_0__.formatDuration)(timeMs);
    var id = Number(trackId);
    var duration = trackDuration ? parseFloat(trackDuration.replace(',', '.')) : 0;
    if (!duration) {
        var error = new Error("No duration provided for a track: ".concat(id));
        // eslint-disable-next-line no-console
        console.error('[tracksPlayer:updateTrackPosition]', error.message, {
            error: error,
        });
        debugger; // eslint-disable-line no-debugger
    }
    var ratio = position / duration;
    var progress = Math.min(100, ratio * 100);
    requestAnimationFrame(function () {
        dataset.position = (0,_helpers_floatToStr__WEBPACK_IMPORTED_MODULE_3__.floatToStr)(position);
        dataset.progress = (0,_helpers_floatToStr__WEBPACK_IMPORTED_MODULE_3__.floatToStr)(progress);
        trackNode.style.setProperty('--progress', dataset.progress);
        if (timeNode) {
            timeNode.innerText = timeFormatted;
        }
    });
    _localTrackInfoDb__WEBPACK_IMPORTED_MODULE_1__.localTrackInfoDb.updatePosition(id, position);
    // TODO: Update the floating player if isCurrent?
    return { position: position, duration: duration, progress: progress };
}
function floatingPlayerUpdate(data) {
    var floatingPlayerState = data.floatingPlayerState, activePlayerData = data.activePlayerData;
    var id = activePlayerData.id;
    var trackNode = currentTrackPlayer;
    if (!trackNode || Number(trackNode.dataset.trackId) !== id) {
        trackNode = getTrackNode(id);
    }
    if (!trackNode) {
        return;
    }
    // const isCurrent = trackNode === currentTrackPlayer;
    var _a = floatingPlayerState.position, position = _a === void 0 ? 0 : _a, _b = floatingPlayerState.progress, progress = _b === void 0 ? 0 : _b, status = floatingPlayerState.status;
    var dataset = trackNode.dataset;
    var timeNode = trackNode.querySelector('.time');
    var timeMs = Math.floor(position * 1000);
    var timeFormatted = (0,_helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_0__.formatDuration)(timeMs);
    requestAnimationFrame(function () {
        if (status) {
            dataset.status = status;
        }
        else {
            delete dataset.status;
        }
        dataset.position = (0,_helpers_floatToStr__WEBPACK_IMPORTED_MODULE_3__.floatToStr)(position);
        dataset.progress = (0,_helpers_floatToStr__WEBPACK_IMPORTED_MODULE_3__.floatToStr)(progress);
        trackNode.style.setProperty('--progress', dataset.progress);
        if (timeNode) {
            timeNode.innerText = timeFormatted;
        }
    });
    // calculateAndUpdateTrackPosition(trackNode, position, isCurrent); // Is it required here?
    // TODO: Update the floating player if isCurrent?
}
function floatingPlayerPlay(data) {
    var 
    // floatingPlayerState,
    activePlayerData = data.activePlayerData;
    if (!currentTrackPlayer) {
        throw new Error('No current track player node!');
    }
    var dataset = currentTrackPlayer.dataset;
    var id = Number(dataset.trackId);
    if (id !== activePlayerData.id) {
        throw new Error('Wrong active track id!');
    }
    requestAnimationFrame(function () {
        dataset.status = 'playing';
    });
}
function floatingPlayerStop(data) {
    var 
    // floatingPlayerState, // ???
    activePlayerData = data.activePlayerData;
    if (!currentTrackPlayer) {
        throw new Error('No current track player node!');
    }
    var dataset = currentTrackPlayer.dataset;
    var id = Number(dataset.trackId);
    if (id !== activePlayerData.id) {
        throw new Error('Wrong active track id!');
    }
    requestAnimationFrame(function () {
        delete dataset.status;
    });
}
function getTrackNode(id) {
    var players = Array.from(allPlayers);
    var trackNode = players.find(function (it) { return Number(it.dataset.trackId) === id; });
    return trackNode;
}
function stopPreviousPlayer() {
    if (currentTrackPlayer) {
        var dataset_1 = currentTrackPlayer.dataset;
        requestAnimationFrame(function () {
            currentTrackPlayer.classList.toggle('current', false);
            delete dataset_1.status;
            delete dataset_1.loaded;
            delete dataset_1.error;
        });
    }
}
function updateTrackPlayedCount(trackNode, playedCount, _isCurrent) {
    var dataset = trackNode.dataset;
    var trackId = dataset.trackId;
    var id = Number(trackId);
    if (!id) {
        throw new Error('No current track id!');
    }
    var updatedTrackInfo = _localTrackInfoDb__WEBPACK_IMPORTED_MODULE_1__.localTrackInfoDb.updatePlayedCount(id, playedCount);
    var updatedPlayedCount = updatedTrackInfo.playedCount;
    var strValue = (0,_helpers_CommonHelpers__WEBPACK_IMPORTED_MODULE_0__.quoteHtmlAttr)(String(updatedPlayedCount));
    var valueNode = trackNode.querySelector('#played_count');
    // Update counter in the document...
    if (valueNode) {
        var parent_1 = valueNode.closest('.track-played-count[data-played-count]');
        requestAnimationFrame(function () {
            valueNode.innerText = strValue;
            if (parent_1) {
                parent_1.dataset.playedCount = strValue;
            }
        });
    }
    // TODO: Update value in the floating player?
}
function updateIncrementCallback(data) {
    var count = data.count, 
    // floatingPlayerState,
    activePlayerData = data.activePlayerData;
    var trackNode = getTrackNode(activePlayerData.id);
    var isCurrent = trackNode === currentTrackPlayer;
    if (trackNode) {
        updateTrackPlayedCount(trackNode, count, isCurrent);
    }
}
/** Play button click handler */
function trackPlayHandler(ev) {
    var controlNode = ev.currentTarget;
    var trackNode = controlNode.closest('.track-player');
    // Reset previous player
    if (currentTrackPlayer && currentTrackPlayer !== trackNode) {
        stopPreviousPlayer();
    }
    var dataset = trackNode.dataset;
    var id = Number(dataset.trackId);
    var playingId = _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.getActiveTrackId();
    var isFloatingPlaying = _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.isPlaying();
    if (isFloatingPlaying) {
        // Pause playback
        _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.pauseCurrentPlayer();
        if (playingId === id) {
            // Return -- just pause current track
            return;
        }
    }
    // Clear all tracks active status?
    requestAnimationFrame(function () {
        allPlayers.forEach(function (it) {
            if (it !== trackNode && it.classList.contains('current')) {
                it.classList.toggle('current', false);
            }
        });
        trackNode.classList.toggle('current', true);
    });
    currentTrackPlayer = trackNode;
    var position = parseFloat((dataset.position || '0').replace(',', '.'));
    _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.setActiveTrack(trackNode, position);
    _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.playCurrentPlayer();
    // Show floating player if has been hidden
    if (!isFloatingPlaying) {
        _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.showFloatingPlayer();
    }
}
function updateTrackFavoriteInDataset(trackNode, isFavorite) {
    var dataset = trackNode.dataset;
    var favorite = dataset.favorite;
    var isCurrentFavorite = Boolean(favorite);
    if (isFavorite !== isCurrentFavorite) {
        requestAnimationFrame(function () {
            if (isFavorite) {
                dataset.favorite = TRUE;
            }
            else {
                delete dataset.favorite;
            }
        });
    }
}
function updateSingleFavoriteCallback(_a) {
    var id = _a.id, favorite = _a.favorite;
    var trackNode = getTrackNode(id);
    if (trackNode) {
        updateTrackFavoriteInDataset(trackNode, favorite);
    }
}
function updateFavoritesCallback(_a) {
    var favorites = _a.favorites;
    allPlayers.forEach(function (trackNode) {
        var dataset = trackNode.dataset;
        var trackId = dataset.trackId;
        var id = Number(trackId);
        var isFavorite = favorites.includes(id);
        updateTrackFavoriteInDataset(trackNode, isFavorite);
    });
}
function initTrackPlayerNodeControls(trackNode) {
    var dataset = trackNode.dataset;
    var trackId = dataset.trackId;
    var id = Number(trackId || '');
    // Set controls' handlers
    var controls = trackNode.querySelectorAll('.track-control');
    controls.forEach(function (node) {
        var dataset = node.dataset;
        var inited = dataset.inited, controlId = dataset.controlId;
        if (inited) {
            return;
        }
        if (controlId === 'toggleFavorite') {
            node.addEventListener('click', function () { return _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.toggleFavoriteById(id); });
        }
        if (controlId === 'play') {
            node.addEventListener('click', trackPlayHandler);
        }
        dataset.inited = TRUE;
    });
    dataset.inited = TRUE;
}
function initTrackPlayerNode(trackNode) {
    var _a;
    var activePlayerData = _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.activePlayerData;
    var dataset = trackNode.dataset;
    var inited = dataset.inited, trackId = dataset.trackId, // "1"
    trackMediaUrl = dataset.trackMediaUrl;
    var id = Number(trackId || '');
    if (!id || inited || !trackMediaUrl) {
        return;
    }
    var hasServerData = window.isAuthenticated;
    var isCurrent = (activePlayerData === null || activePlayerData === void 0 ? void 0 : activePlayerData.id) == id;
    var trackInfo = _localTrackInfoDb__WEBPACK_IMPORTED_MODULE_1__.localTrackInfoDb.getById(id);
    var favorite = hasServerData ? Boolean(dataset.favorite) : !!(trackInfo === null || trackInfo === void 0 ? void 0 : trackInfo.favorite);
    /* // DEBUG
     * if (trackInfo) {
     *   console.log('[tracksPlayer:initTrackPlayerNode] start', id, {
     *     hasServerData,
     *     isCurrent,
     *     trackInfo,
     *     favorite,
     *     inited,
     *     trackId, // "1"
     *     trackMediaUrl, // "/media/samples/gr-400x225.jpg"
     *     dataset,
     *     trackNode,
     *   });
     *   if (id === 5) {
     *     debugger;
     *   }
     * }
     */
    if (trackInfo) {
        if (!hasServerData) {
            // If no server data then update favorite from the local db
            if (favorite) {
                updateTrackFavoriteInDataset(trackNode, trackInfo.favorite);
            }
        }
        // TODO: Get position from the server (dataset)
        var duration = calculateAndUpdateTrackPosition(trackNode, trackInfo.position || 0, isCurrent).duration;
        var playedCount = Number(((_a = trackNode.querySelector('.track-played-count')) === null || _a === void 0 ? void 0 : _a.dataset.playedCount) || '0');
        // Update the local db date...
        if (activePlayerData) {
            activePlayerData.favorite = favorite;
            activePlayerData.duration = duration;
        }
        /* TODO: Update local data (favorite, playedCount) from track node dataset?
         * - id
         * - favorite
         * - lastPlayed
         * - lastUpdated
         * - playedCount
         * - position
         */
        var hasChangedData = playedCount !== trackInfo.playedCount || favorite !== trackInfo.favorite;
        if (hasChangedData) {
            trackInfo.playedCount = playedCount;
            trackInfo.favorite = favorite;
            _localTrackInfoDb__WEBPACK_IMPORTED_MODULE_1__.localTrackInfoDb.save(trackInfo);
        }
    }
    if (isCurrent) {
        activePlayerData.title = dataset.trackTitle || '';
        currentTrackPlayer = trackNode;
        requestAnimationFrame(function () {
            trackNode.classList.toggle('current', true);
        });
        floatingPlayerUpdate({ floatingPlayerState: _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.state, activePlayerData: activePlayerData });
    }
    initTrackPlayerNodeControls(trackNode);
}
function initTracksPlayerWrapper(domNode) {
    if (domNode === void 0) { domNode = document.body; }
    allPlayers = domNode.querySelectorAll('.track-player[data-track-media-url]');
    allPlayers.forEach(initTrackPlayerNode);
    _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.callbacks.addPlayStartCallback(floatingPlayerPlay);
    _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.callbacks.addPlayStopCallback(floatingPlayerStop);
    _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.callbacks.addUpdateCallback(floatingPlayerUpdate);
    _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.callbacks.addIncrementCallback(updateIncrementCallback);
    _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.callbacks.addFavoritesCallback(updateFavoritesCallback);
    _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.floatingPlayer.callbacks.addFavoriteCallback(updateSingleFavoriteCallback);
}


/***/ }),

/***/ "./src/assets/helpers/CommonHelpers.js":
/*!*********************************************!*\
  !*** ./src/assets/helpers/CommonHelpers.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NOOP: () => (/* binding */ NOOP),
/* harmony export */   addCssStyle: () => (/* binding */ addCssStyle),
/* harmony export */   addScript: () => (/* binding */ addScript),
/* harmony export */   compareArrays: () => (/* binding */ compareArrays),
/* harmony export */   decodeQuery: () => (/* binding */ decodeQuery),
/* harmony export */   deleteAllCookies: () => (/* binding */ deleteAllCookies),
/* harmony export */   formatDuration: () => (/* binding */ formatDuration),
/* harmony export */   getApproxSize: () => (/* binding */ getApproxSize),
/* harmony export */   getAsyncHash: () => (/* binding */ getAsyncHash),
/* harmony export */   getCookie: () => (/* binding */ getCookie),
/* harmony export */   getErrorText: () => (/* binding */ getErrorText),
/* harmony export */   htmlToElement: () => (/* binding */ htmlToElement),
/* harmony export */   htmlToElements: () => (/* binding */ htmlToElements),
/* harmony export */   makeQuery: () => (/* binding */ makeQuery),
/* harmony export */   normalizedFloatStr: () => (/* binding */ normalizedFloatStr),
/* harmony export */   parseQuery: () => (/* binding */ parseQuery),
/* harmony export */   processMultipleRequestErrors: () => (/* binding */ processMultipleRequestErrors),
/* harmony export */   quoteHtmlAttr: () => (/* binding */ quoteHtmlAttr),
/* harmony export */   setCookie: () => (/* binding */ setCookie),
/* harmony export */   setMultipleSelectValues: () => (/* binding */ setMultipleSelectValues),
/* harmony export */   updateNodeContent: () => (/* binding */ updateNodeContent)
/* harmony export */ });
// @ts-check

function NOOP() {}

/** Compare two arrays with scalar (number, string, boolean) values
 * @param {(number | string | boolean)[]} a1
 * @param {(number | string | boolean)[]} a2
 * @return {boolean}
 */
function compareArrays(a1, a2) {
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
function getErrorText(error) {
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
function quoteHtmlAttr(str, preserveCR) {
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
function htmlToElement(html) {
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
function htmlToElements(html) {
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
function updateNodeContent(node, content) {
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
function decodeQuery(qs, sep, eq, options) {
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
function parseQuery(search) {
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
function makeQuery(params, opts = {}) {
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
function addScript(url) {
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
function addCssStyle(url) {
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
function setMultipleSelectValues(node, values) {
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
function processMultipleRequestErrors(resList) {
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
function normalizedFloatStr(n, opts = {}) {
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
function getApproxSize(size, opts = {}) {
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
function formatDuration(time) {
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
function getAsyncHash(str) {
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
function getCookie(cookieId) {
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
function setCookie(id, val, maxAgeSecs) {
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

function deleteAllCookies() {
  document.cookie.split(';').forEach((cookie) => {
    const eqPos = cookie.indexOf('=');
    const name = eqPos > -1 ? cookie.substring(0, eqPos) : cookie;
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT';
  });
}


/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry needs to be wrapped in an IIFE because it needs to be in strict mode.
(() => {
"use strict";
var __webpack_exports__ = {};
/*!*****************************!*\
  !*** ./src/assets/index.ts ***!
  \*****************************/
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _checkProjectVersion__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./checkProjectVersion */ "./src/assets/checkProjectVersion.ts");
/* harmony import */ var _track_blocks_tracksPlayer__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./track-blocks/tracksPlayer */ "./src/assets/track-blocks/tracksPlayer.ts");
/* harmony import */ var _entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./entities/FloatingPlayer/floatingPlayer */ "./src/assets/entities/FloatingPlayer/floatingPlayer.ts");
/* harmony import */ var _processTextContent__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./processTextContent */ "./src/assets/processTextContent.ts");
/* harmony import */ var _cookies_banner_cookiesBanner__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./cookies-banner/cookiesBanner */ "./src/assets/cookies-banner/cookiesBanner.ts");
/**
 * @desc Main entry point module (scripts)
 * @module src/assets/index.ts
 * @changed 2025.02.24, 22:12
 */





(0,_cookies_banner_cookiesBanner__WEBPACK_IMPORTED_MODULE_4__.initCookiesBanner)();
(0,_checkProjectVersion__WEBPACK_IMPORTED_MODULE_0__.checkProjectVersion)();
(0,_processTextContent__WEBPACK_IMPORTED_MODULE_3__.processTextContent)();
(0,_track_blocks_tracksPlayer__WEBPACK_IMPORTED_MODULE_1__.initTracksPlayerWrapper)();
(0,_entities_FloatingPlayer_floatingPlayer__WEBPACK_IMPORTED_MODULE_2__.initFloatingPlayer)();

})();

// This entry needs to be wrapped in an IIFE because it needs to be isolated against other entry modules.
(() => {
/*!********************************!*\
  !*** ./src/assets/styles.scss ***!
  \********************************/
// extracted by mini-css-extract-plugin
})();

/******/ })()
;
//# sourceMappingURL=scripts.js.map