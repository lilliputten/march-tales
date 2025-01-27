# -*- coding:utf-8 -*-

import os.path
import json
import posixpath

from .appEnv import (
    BASE_DIR,
    appEnv,
)

# Timezone (set `TZ_HOURS` to hours value to adjust date representation to corresponding timezone)
TZ_HOURS = appEnv.int('TZ_HOURS_OFFSET', 0)

APK_FOLDER = appEnv.str('APK_FOLDER', 'static/downloads/apk')
APK_JSON_FILE = appEnv.str('APK_JSON_FILE', posixpath.join(APK_FOLDER, 'output-metadata.json'))
APK_DOWNLOAD_FILE = ''
APK_DOWNLOAD_VERSION = ''
APK_DOWNLOAD_SIZE = 0

try:
    # if os.path.isfile(APK_JSON_FILE):
    #     pass
    filepath = posixpath.join(BASE_DIR, APK_JSON_FILE)
    with open(filepath) as f:
        data = json.load(f)
        element = data['elements'][0]
        APK_DOWNLOAD_FILE = posixpath.join(APK_FOLDER, element['outputFile'])
        apkPath = posixpath.join(BASE_DIR, APK_DOWNLOAD_FILE)
        APK_DOWNLOAD_SIZE = os.stat(apkPath).st_size
        APK_DOWNLOAD_VERSION = element['versionName']
except Exception as err:
    print('Can get APK_DOWNLOAD_FILE from APK_JSON_FILE:', repr(err))
