import posixpath

from core.djangoConfig import MEDIA_TRACKS_FOLDER
from core.helpers.time import getTimeFormat


def getAudioTrackFolderName():
    dateId = getTimeFormat('dateId')
    return posixpath.join(MEDIA_TRACKS_FOLDER, dateId)
