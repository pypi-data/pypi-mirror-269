from os import path
from yt_dlp import YoutubeDL
from ..scripts.eo import Okeys
from urllib.parse import unquote
from urllib.parse import urlparse
#======================================================================


class SMessages:
    def __init__(self, **kwargs):
        self.errors = kwargs.get("errors", None)
        self.result = kwargs.get("result", None)

#======================================================================

class Filename:

    async def get01(filelink):
        try:
            findoutne = urlparse(filelink)
            filenameo = path.basename(findoutne.path)
            filenames = unquote(filenameo)
            return SMessages(result=filenames)
        except Exception as errors:
            return SMessages(errors=errors)

#======================================================================

    async def get02(filelink, command):
        with YoutubeDL(command) as ydl:
            try:
                mainos = Okeys.DATA01
                meawes = ydl.extract_info(filelink, download=False)
                moonus = ydl.prepare_filename(meawes, outtmpl=mainos)
                return SMessages(result=moonus)
            except Exception as errors:
                return SMessages(result="Unknown.tmp", errors=errors)

#======================================================================
