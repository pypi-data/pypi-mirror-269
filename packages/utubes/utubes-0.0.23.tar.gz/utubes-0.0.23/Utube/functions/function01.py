import os, asyncio
from ..scripts import Okeys
from yt_dlp import YoutubeDL, DownloadError
#==========================================================================

class SMessages:
    def __init__(self, **kwargs):
        self.status = kwargs.get('status', True)
        self.errors = kwargs.get('errors', None)
        self.result = kwargs.get('result', None)

#==========================================================================

class DownloadER:

    async def metadata(link, command):
        with YoutubeDL(command) as ydl:
            try:
                moonus = ydl.extract_info(link, download=False)
                return SMessages(result=moonus)
            except Exception as errors:
                return SMessages(errors=errors)

#==========================================================================

    async def extracts(link, command):
        with YoutubeDL(command) as ydl:
            try:
                moonus = ydl.extract_info(link, download=False)
                return SMessages(result=moonus)
            except Exception as errors:
                return SMessages(errors=errors)

#==========================================================================

    async def filename(link, command):
        with YoutubeDL(command) as ydl:
            try:
                mainos = Okeys.DATA01
                meawes = ydl.extract_info(link, download=False)
                moonus = ydl.prepare_filename(meawes, outtmpl=mainos)
                return SMessages(result=moonus)
            except Exception as errors:
                return SMessages(result="Unknown.tmp", errors=errors)

#==========================================================================

    async def download(link, command, progress):
        loop = asyncio.get_event_loop()
        with YoutubeDL(command) as ydl:
            try:
                filelink = [link]
                ydl.add_progress_hook(progress)   
                await loop.run_in_executor(None, ydl.download, filelink)
                return SMessages(status=True)
            except DownloadError as errors:
                return SMessages(status=False, errors=errors)
            except Exception as errors:
                return SMessages(status=False, errors=errors)

#==========================================================================
