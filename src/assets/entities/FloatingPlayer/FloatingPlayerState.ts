export interface FloatingPlayerState {
  lastTimestamp?: number;
  visible?: boolean;
  loaded?: boolean;
  // playing?: boolean;
  status?: 'playing' | 'paused' | 'waiting' | undefined;
  position?: number;
  progress?: number;
  error?: string;
}

const storageFloatingPlayerStateId = 'FloatingPlayerState';

function convertFloatingPlayerStateToJsonStr(data: FloatingPlayerState) {
  return JSON.stringify(data);
}

function convertFloatingPlayerStateFromJsonStr(str: string) {
  return (str ? JSON.parse(str) : {}) as FloatingPlayerState;
}

export function saveFloatingPlayerState(data: FloatingPlayerState) {
  const saveData = { ...data, lastTimestamp: Date.now() };
  delete saveData.error;
  delete saveData.loaded;
  // status?
  const str = convertFloatingPlayerStateToJsonStr(saveData);
  window.localStorage.setItem(storageFloatingPlayerStateId, str);
}

export function loadFloatingPlayerState() {
  const str = window.localStorage.getItem(storageFloatingPlayerStateId);
  return convertFloatingPlayerStateFromJsonStr(str);
}
