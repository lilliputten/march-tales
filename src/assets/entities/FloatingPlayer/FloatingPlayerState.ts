import { floatToStr } from '../../helpers/floatToStr';

type Status = 'playing' | 'paused' | 'waiting';

export interface FloatingPlayerState {
  lastTimestamp?: number; // Timestamp
  visible?: boolean;
  loaded?: boolean;
  status?: Status | undefined;
  position?: number;
  progress?: number;
  error?: string;
}

const storageFloatingPlayerStateId = 'FloatingPlayerState';

function convertFloatingPlayerStateFromJsonStr(str: string) {
  if (!str) {
    return {};
  }
  try {
    const list = str.split(',');
    const [
      // Keep the order!
      lastTimestamp,
      visible,
      status,
      position,
      progress,
    ] = list;
    const data: FloatingPlayerState = {
      // Keep the order!
      lastTimestamp: lastTimestamp ? Number(lastTimestamp) * 1000 : undefined, // Timestamp
      visible: visible ? Boolean(visible) : undefined,
      status: status ? (String(status) as Status) : undefined,
      position: position ? Number(position) : undefined,
      progress: progress ? Number(progress) : undefined,
    };
    return data;
  } catch (
    err // eslint-disable-line @typescript-eslint/no-unused-vars
  ) {
    // eslint-disable-next-line no-console
    console.warn('[FloatingPlayerState:convertFloatingPlayerStateFromJsonStr] Parse error', {
      str,
      err,
    });
    return {};
  }
}

function convertFloatingPlayerStateToJsonStr(data: FloatingPlayerState) {
  const {
    // Keep the order!
    lastTimestamp,
    visible,
    status,
    position,
    progress,
  } = data;
  const list = [
    // Keep the order!
    lastTimestamp ? Math.round(lastTimestamp / 1000) : undefined, // Timestamp
    visible ? Number(visible) : undefined, // Boolean
    status ? status : undefined,
    position ? floatToStr(position) : undefined,
    progress ? floatToStr(progress) : undefined,
  ];
  const str = list.join(',').replace(/,+$/, '');
  return str;
}

export function saveFloatingPlayerState(data: FloatingPlayerState) {
  const saveData = { ...data, lastTimestamp: Date.now() };
  const str = convertFloatingPlayerStateToJsonStr(saveData);
  window.localStorage.setItem(storageFloatingPlayerStateId, str);
}

export function loadFloatingPlayerState() {
  const str = window.localStorage.getItem(storageFloatingPlayerStateId);
  return convertFloatingPlayerStateFromJsonStr(str);
}
