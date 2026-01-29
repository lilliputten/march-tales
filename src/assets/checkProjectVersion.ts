/** Get major and minor versions in form '1.2' from a string 'march-tales v.1.2.20 / 2025.02.20 15:22:00 +0300' */
function getMinorVersionFromProjectInfo(info?: string | null) {
  if (!info) {
    return undefined;
  }
  try {
    const match = info.match(/^\S+ v\.(\d+\.\d+)/);
    if (match) {
      const v = match[1];
      return v;
    }
  } catch (
    _e // eslint-disable-line @typescript-eslint/no-unused-vars
  ) {
    // NOOP
    return undefined;
  }
}

export function checkProjectVersion() {
  const oldInfo = window.localStorage.getItem('projectInfo');
  const newInfo = window.projectInfo;
  // eslint-disable-next-line no-console
  console.log('[checkProjectVersion]', newInfo);
  if (newInfo && newInfo !== oldInfo) {
    const oldVersion = getMinorVersionFromProjectInfo(oldInfo);
    const newVersion = getMinorVersionFromProjectInfo(newInfo);
    if (newVersion !== oldVersion) {
      // TODO: To clear some stored data etc?
      // eslint-disable-next-line no-console
      console.warn(
        '[checkProjectVersion] Project version has changed',
        newVersion,
        '<->',
        oldVersion,
        {
          oldInfo,
          newInfo,
          oldVersion,
          newVersion,
        },
      );
      // debugger; // eslint-disable-line no-debugger
    }
    window.localStorage.setItem('projectInfo', newInfo);
  }
}
