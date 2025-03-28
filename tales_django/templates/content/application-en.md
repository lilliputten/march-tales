## The Application

The **Flutter-based mobile app** is the main component of the project, and offers an immersive listenning experience with robust audio controls.

## Key Features:

- **Audio Playback**: Powered by **Just Audio**, with background service support for notification controls.
- **Favorites Management**: Local storage or cloud sync via the API server.
- **Internationalization & Theming**: Multi-language support and basic customization options.

## Audio Playback

Both the website and the mobile device have relatively identical audio player behavior:

- The hideable floating player on the bottom of the page.
- Both the website and the mobile application remembers the playback position of each track so that playback can be resumed at any time.
- Playback positions are stored locally or on the server if the user is logged in.
- It supports endless playback when tracks are played one after the other. (Since the application is still in MVP status, it uses fairly simple logic to determine the next track to play.)

## Seamless Cross-Device Experience

**Local vs. Synced Data**:

- **Web/Mobile**: Favorites can be stored locally without an account.
- **Authorized Users**: Sync preferences across devices via the API server.

**Unified Backend**: Both web and mobile clients share the same API server for data consistency.
