from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
#=======================================================================================

class SMessages:
    def __init__(self, **kwargs):
        self.width = kwargs.get("width", 0)
        self.height = kwargs.get("height", 0)
        self.duration = kwargs.get("duration", 0)

#=======================================================================================

class Metadatas:

    async def width(flocation):
        metadato = createParser(flocation)
        metadata = extractMetadata(metadato)
        if metadata == None:
            return 0
        width = metadata.get("width") if metadata.has("width") else 0
        return width

#=======================================================================================

    async def height(flocation):
        metadato = createParser(flocation)
        metadata = extractMetadata(metadato)
        if metadata == None:
            return 0
        height = metadata.get("height") if metadata.has("height") else 0
        return height

#=======================================================================================

    async def duration(flocation):
        metadato = createParser(flocation)
        metadata = extractMetadata(metadato)
        if metadata == None:
            return 0
        duration = metadata.get("duration").seconds if metadata.has("duration") else 0
        return duration

#=======================================================================================

    async def get01(flocation):
        metadato = createParser(flocation)
        metadata = extractMetadata(metadato)
        if metadata == None:
            return 0, 0, 0
        width = metadata.get("width") if metadata.has("width") else 0
        height = metadata.get("height") if metadata.has("height") else 0
        duration = metadata.get("duration").seconds if metadata.has("duration") else 0
        return width, height, duration

#=======================================================================================

    async def get02(flocation):
        metadato = createParser(flocation)
        metadata = extractMetadata(metadato)
        if metadata == None:
            return SMessages(width=0, height=0, duration=0)
        width = metadata.get("width") if metadata.has("width") else 0
        height = metadata.get("height") if metadata.has("height") else 0
        duration = metadata.get("duration").seconds if metadata.has("duration") else 0
        return SMessages(width=width, height=height, duration=duration)

#=======================================================================================
