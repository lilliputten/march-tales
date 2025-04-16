import { acceptedCookiesId } from '../constants/acceptedCookiesId';
import { deleteAllCookies, setCookie } from '../helpers/CommonHelpers';

let eventHandler: () => void;

function updateBannerGeometry(bannerNode: HTMLElement) {
  const footerNode = document.querySelector<HTMLElement>('.template-footer');
  if (!bannerNode || !footerNode) {
    return;
  }
  const bannerHeight = bannerNode.clientHeight;
  footerNode.style.marginBottom = `${bannerHeight}px`;
}

function handleAccept(event: Event) {
  const buttonNode = event.currentTarget as HTMLButtonElement;
  const bannerNode = buttonNode.closest<HTMLElement>('.cookies-banner');
  const value = 'allowed';
  window.localStorage.setItem('cookies', value);
  setCookie(acceptedCookiesId, value);
  hideBanner(bannerNode!);
}

function handleReject(event: Event) {
  const buttonNode = event.currentTarget as HTMLButtonElement;
  const bannerNode = buttonNode.closest<HTMLElement>('.cookies-banner');
  const value = '';
  window.localStorage.setItem(acceptedCookiesId, value);
  deleteAllCookies();
  setCookie(acceptedCookiesId, '');
  hideBanner(bannerNode!);
}

function initActiveBanner(bannerNode: HTMLElement) {
  if (eventHandler) {
    window.removeEventListener('resize', eventHandler);
    window.removeEventListener('orientationchange', eventHandler);
  }
  eventHandler = updateBannerGeometry.bind(bannerNode);
  window.addEventListener('resize', eventHandler);
  window.addEventListener('orientationchange', eventHandler);
  updateBannerGeometry(bannerNode);
  // Set button handlers...
  bannerNode
    .querySelector<HTMLButtonElement>('button#Accept')
    ?.addEventListener('click', handleAccept);
  bannerNode
    .querySelector<HTMLButtonElement>('button#Reject')
    ?.addEventListener('click', handleReject);
  bannerNode.classList.toggle('visible', true);
}

function hideBanner(bannerNode?: HTMLElement) {
  if (bannerNode) {
    bannerNode.remove();
  }
  document.body.classList.add('no-cookies-banner');
  if (eventHandler) {
    window.removeEventListener('resize', eventHandler);
    window.removeEventListener('orientationchange', eventHandler);
  }
}

export function initCookiesBanner() {
  const bannerNode = document.querySelector<HTMLElement>('.cookies-banner');
  if (!bannerNode) {
    return;
  }
  const cookiesBannerStr = window.localStorage.getItem(acceptedCookiesId);
  if (cookiesBannerStr == null) {
    initActiveBanner(bannerNode);
  } else {
    hideBanner(bannerNode);
  }
}
