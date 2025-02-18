import { ActivePlayerData } from './ActivePlayerData';

export function getActivePlayerDataFromTrackNode(trackNode: HTMLElement) {
  const { dataset } = trackNode;
  const id = Number(dataset.trackId);
  const favorite = Boolean(dataset.favorite);
  // const status = dataset.status;
  const duration = parseFloat((dataset.trackDuration || '0').replace(',', '.'));
  // const position = parseFloat((dataset.position || '0').replace(',', '.'));
  const mediaUrl = dataset.trackMediaUrl || '';
  const imageNode = trackNode.querySelector<HTMLImageElement>('img.card-img');
  const imageUrl = imageNode?.getAttribute('src') || '';
  const title = dataset.trackTitle || '';
  const activePlayerData: ActivePlayerData = {
    id,
    title,
    imageUrl,
    mediaUrl,
    duration,
    favorite,
  };
  return activePlayerData;
}
