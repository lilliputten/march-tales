import { ActivePlayerData } from './ActivePlayerData';

export function getActivePlayerDataFromTrackNode(trackNode: HTMLElement) {
  const { dataset } = trackNode;
  const id = Number(dataset.trackId);
  // const status = dataset.status;
  const duration = parseFloat((dataset.trackDuration || '0').replace(',', '.'));
  // const position = parseFloat((dataset.position || '0').replace(',', '.'));
  const mediaUrl = dataset.trackMediaUrl;
  const imageNode = trackNode.querySelector<HTMLImageElement>('img.card-img');
  const imageUrl = imageNode?.getAttribute('src');
  const titleNode = trackNode.querySelector<HTMLElement>('.post-title');
  const title = titleNode?.innerHTML;
  const activePlayerData: ActivePlayerData = {
    id,
    title,
    imageUrl,
    mediaUrl,
    duration,
    // position,
    // status,
  };
  // const link = titleNode?.getAttribute('href');
  console.log('[getActivePlayerDataFromTrackNode]', {
    activePlayerData,
    id, // 6
    duration, // 17.972245
    mediaUrl,
    imageUrl, // "/media/samples/Тест_кириллицы.png"
    trackNode, // article.big-tracks-list-item.card.no-bg.mb-4.track-player.current
    title, // "Новый трек"
    // status,
    // trackNode,
    // dataset,
  });
  // TODO: Store in the local storage the last status (playing, paused etc) and last activity time
  return activePlayerData;
}
