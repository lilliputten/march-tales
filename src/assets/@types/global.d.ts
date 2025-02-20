declare global {
  interface Window {
    projectInfo?: string;
    isAuthenticated?: boolean;
    hasFavoriteTracks?: boolean;
  }
}

export {};
