from ..scripts.eu import EBoxo
from ..scripts.en import Scripted
#=================================================================================================

class SMessages:
    def __init__(self, **kwargs):
        self.formatid = kwargs.get("formatid", Scripted.DATA01)
        self.filesize = kwargs.get("filesize", Scripted.DATA01)
        self.filename = kwargs.get("filename", Scripted.DATA01)
        self.duration = kwargs.get("duration", Scripted.DATA01)
        self.formatQu = kwargs.get("formatQu", Scripted.DATA01)
        self.formatex = kwargs.get("formatex", Scripted.DATA01)

#=================================================================================================

class FormatoR:

    async def format01(result):
        fename = str(result.get("title"))
        durion = result.get(EBoxo.DATA02) if EBoxo.DATA02 in result else None
        return SMessages(filename=fename, duration=durion)

#=================================================================================================
    
    async def format02(result): # YTENGINE
        form01 = result.get(EBoxo.DATA08) # FORMATEXT
        form02 = result.get(EBoxo.DATA03) # FORMATIDS
        form03 = result.get(EBoxo.DATA04) # FORMATSRG
        size01 = result.get(EBoxo.DATA06) # FILESIZE1
        size02 = result.get(EBoxo.DATA07) # FILESIZE2
        form04 = result.get(EBoxo.DATA05) if form03 == None else form03
        sizesz = size01 if size01 else size02 if size02 else Scripted.DATA01
        return SMessages(formatex=form01, formatid=form02, formatQu=form04, filesize=sizesz)

#=================================================================================================

    async def format03(result): # JIOCINEMA 
        form01 = result.get(EBoxo.DATA08) # FORMATEXT
        form02 = result.get(EBoxo.DATA03) # FORMATIDS
        form03 = result.get(EBoxo.DATA04) # FORMATSRG
        size01 = result.get(EBoxo.DATA06) # FILESIZE1
        size02 = result.get(EBoxo.DATA07) # FILESIZE2
        string = result.get(EBoxo.DATA05) if form03 == None else form03
        sizesz = size01 if size01 else size02 if size02 else Scripted.DATA01
        return SMessages(formatex=form01, formatid=form02, formatQu=form04, filesize=sizesz)

#=================================================================================================
