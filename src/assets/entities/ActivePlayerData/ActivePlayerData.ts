import { floatToStr } from '../../helpers/floatToStr';

export interface ActivePlayerData {
  id: number;
  title: string;
  imageUrl: string;
  mediaUrl: string;
  duration: number;
  favorite: boolean;
}

const storageActivePlayerDataId = 'ActivePlayerData';

function convertActivePlayerDataFromJsonStr(str: string) {
  if (!str) {
    return undefined;
  }
  try {
    const raw = JSON.parse(str);
    // const list = str.split(',');
    const {
      // Keep the order!
      id,
      title,
      imageUrl,
      mediaUrl,
      duration,
      favorite,
    } = raw;
    const data: ActivePlayerData = {
      // Keep the order!
      id: id ? Number(id) : 0,
      title: title ? String(title) : '',
      imageUrl: imageUrl ? String(imageUrl) : '',
      mediaUrl: mediaUrl ? String(mediaUrl) : '',
      duration: duration ? Number(duration) : 0,
      favorite: Boolean(favorite),
    };
    return data;
  } catch (
    err // eslint-disable-line @typescript-eslint/no-unused-vars
  ) {
    // eslint-disable-next-line no-console
    console.warn('[ActivePlayerData:storageActivePlayerDataId] Parse error', {
      str,
      err,
    });
    return undefined;
  }
}

function convertActivePlayerDataToJsonStr(data: ActivePlayerData) {
  return JSON.stringify(data);
}

export function saveActivePlayerData(data?: ActivePlayerData) {
  const str = data ? convertActivePlayerDataToJsonStr(data) : '';
  window.localStorage.setItem(storageActivePlayerDataId, str);
}

export function loadActivePlayerData() {
  const str = window.localStorage.getItem(storageActivePlayerDataId);
  return convertActivePlayerDataFromJsonStr(str);
}
