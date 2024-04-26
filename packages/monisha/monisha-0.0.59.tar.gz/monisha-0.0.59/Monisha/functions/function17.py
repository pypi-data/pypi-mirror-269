import os, random
from urllib.parse import unquote
from urllib.parse import urlparse
#=========================================================================


class SMessages:
    def __init__(self, **kwargs):
        self.errors = kwargs.get("errors", None)
        self.result = kwargs.get("result", None)
        self.filename = kwargs.get("filename", None)
        self.extension = kwargs.get("extension", None)

#=========================================================================

class Filename:

    async def get01(extension=None):
        mainos = str(random.randint(10000, 100000000000000))
        moonus = mainos + extension if extension else mainos
        return moonus

#=========================================================================

    async def get02(filename):
        nameas = str(filename)
        cnames = os.path.splitext(nameas)[0]
        exexon = os.path.splitext(nameas)[1]
        exoexo = exexon if exexon else ".tmp"
        moonus = finame if finame else "Unknown"
        return SMessages(filename=moonus, extension=exoexo)

#=========================================================================

    async def get03(filelink):
        try:
            findoutne = urlparse(filelink)
            filenameo = os.path.basename(findoutne.path)
            filenames = unquote(filenameo)
            return SMessages(result=filenames)
        except Exception as errors:
            return SMessages(result="Unknown.tmp", errors=errors)

#=========================================================================
