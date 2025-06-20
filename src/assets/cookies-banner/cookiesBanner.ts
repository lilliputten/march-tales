import { acceptedCookiesId } from '../constants/acceptedCookiesId';
import { deleteAllCookies, setCookie } from '../helpers/CommonHelpers';

let bannerNode: null | HTMLElement = null;

function updateBannerGeometry() {
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

function initActiveBanner() {
  if (!bannerNode) {
    return;
  }
  bannerNode.classList.toggle('visible', true);
  updateBannerGeometry();
  window.addEventListener('resize', updateBannerGeometry);
  window.addEventListener('orientationchange', updateBannerGeometry);
  // Set button handlers...
  bannerNode
    .querySelector<HTMLButtonElement>('button#Accept')
    ?.addEventListener('click', handleAccept);
  bannerNode
    .querySelector<HTMLButtonElement>('button#Reject')
    ?.addEventListener('click', handleReject);
}

function hideBanner(bannerNode?: HTMLElement) {
  if (bannerNode) {
    bannerNode.remove();
  }
  document.body.classList.add('no-cookies-banner');
  window.removeEventListener('resize', updateBannerGeometry);
  window.removeEventListener('orientationchange', updateBannerGeometry);
}

export function initCookiesBanner() {
  bannerNode = document.querySelector<HTMLElement>('.cookies-banner');
  if (!bannerNode) {
    return;
  }
  const cookiesBannerStr = window.localStorage.getItem(acceptedCookiesId);
  if (!cookiesBannerStr) {
    initActiveBanner();
  } else {
    hideBanner(bannerNode);
  }
}
