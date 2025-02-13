export function showFloatingPlayer(trackNode: HTMLElement) {
  const { dataset } = trackNode;
  const { trackDuration, trackId } = dataset;
  const id = Number(trackId);
  const duration = parseFloat(trackDuration.replace(',', '.'));
  const imgNode = trackNode.querySelector<HTMLImageElement>('img.card-img');
  const imgUrl = imgNode?.getAttribute('src');
  const titleNode = trackNode.querySelector<HTMLElement>('.post-title');
  const title = titleNode?.innerHTML;
  const link = titleNode?.getAttribute('href');
  console.log('[floatingPlayer:initFloatingPlayer]', {
    id, // 6
    duration, // 17.972245
    imgUrl, // "/media/samples/Тест_кириллицы.png"
    link, // "/tracks/6"
    trackNode, // article.big-tracks-list-item.card.no-bg.mb-4.track-player.current
    title, // "Новый трек"
    // trackNode,
    // dataset,
  });
  // TODO: Store in the local storage the last status (playing, paused etc) and last activity time
  document.body.classList.toggle('withPlayer', true);
}

export function initFloatingPlayer() {
  // console.log('[floatingPlayer:initFloatingPlayer]');
}
