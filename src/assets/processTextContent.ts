function processLink(node: HTMLElement) {
  if (!node.classList.contains('external')) {
    node.classList.add('external');
    node.setAttribute('target', '_blank');
    const nodeIcon = document.createElement('span');
    nodeIcon.classList.add('icon', 'icon-external', 'bi', 'bi-box-arrow-up-right');
    node.appendChild(nodeIcon);
  }
}

function processTextBlock(node: HTMLElement) {
  // Find external links...
  const linkNodes = node.querySelectorAll<HTMLLinkElement>('a[href^="https://"]');
  linkNodes.forEach(processLink);
}

export function processTextContent() {
  const textNodes = document.querySelectorAll<HTMLElement>('.text-content');
  textNodes.forEach(processTextBlock);
}
