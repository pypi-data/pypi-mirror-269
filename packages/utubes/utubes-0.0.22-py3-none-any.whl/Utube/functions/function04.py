import os, random
from ..scripts import Okeys
from yt_dlp import YoutubeDL
from urllib.parse import unquote
from urllib.parse import urlparse
#=========================================================================


class SMessages:
    def __init__(self, **kwargs):
        self.errors = kwargs.get("errors", None)
        self.result = kwargs.get("result", None)

#=========================================================================

class Filename:

    async def get01(extension=None):
        mainos = str(random.randint(10000, 100000000000000))
        moonus = mainos + extension if extension else mainos
        return moonus

#=========================================================================

    async def get02(filelink):
        try:
            findoutne = urlparse(filelink)
            filenameo = os.path.basename(findoutne.path)
            filenames = unquote(filenameo)
            return SMessages(result=filenames)
        except Exception as errors:
            return SMessages(result="Unknown.tmp", errors=errors)

#=========================================================================

    async def get03(filelink, command):
        with YoutubeDL(command) as ydl:
            try:
                mainos = Okeys.DATA01
                meawes = ydl.extract_info(filelink, download=False)
                moonus = ydl.prepare_filename(meawes, outtmpl=mainos)
                return SMessages(result=moonus)
            except Exception as errors:
                return SMessages(result="Unknown.tmp", errors=errors)

#=========================================================================
