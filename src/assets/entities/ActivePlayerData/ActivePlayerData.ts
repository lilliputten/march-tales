export interface ActivePlayerData {
  id: number;
  title: string;
  imageUrl: string;
  mediaUrl: string;
  duration: number;
  favorite: boolean;
  // position: number;
  // status?: string;
}

const storageActivePlayerDataId = 'ActivePlayerData';

function convertActivePlayerDataToJsonStr(data: ActivePlayerData) {
  return JSON.stringify(data);
}

function convertActivePlayerDataFromJsonStr(str: string) {
  return str ? (JSON.parse(str) as ActivePlayerData) : undefined;
}

export function saveActivePlayerData(data?: ActivePlayerData) {
  const str = data ? convertActivePlayerDataToJsonStr(data) : '';
  window.localStorage.setItem(storageActivePlayerDataId, str);
}

export function loadActivePlayerData() {
  const str = window.localStorage.getItem(storageActivePlayerDataId);
  return convertActivePlayerDataFromJsonStr(str);
}
