declare global {
  interface Window {
    LOCAL?: boolean;
    DEBUG?: boolean;
    projectInfo?: string;
    isAuthenticated?: boolean;
    userId?: number;
    hasFavoriteTracks?: boolean;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    AOS: { init: (o: Record<string, any>) => void };
    $: jQuery;
  }
}

export {};
