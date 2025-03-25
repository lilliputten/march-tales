declare global {
  interface Window {
    LOCAL?: boolean;
    DEBUG?: boolean;
    projectInfo?: string;
    isAuthenticated?: boolean;
    hasFavoriteTracks?: boolean;
    AOS: { init: (o: Record<string, any>) => void };
  }
}

export {};
