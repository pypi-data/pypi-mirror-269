
class SMessages:
    def __init__(self, **kwargs):
        self.types = kwargs.get("types", None)
        self.error = kwargs.get("types", None)

#====================================================================

class FMagic:

    def get01(file):
        try:
            from magic import Magic
            mimees = Magic(mime=True)
            mimeos = mimees.from_file(file)
            mimemo = mimeos or "text/plain"
            return SMessages(types=mimemo)
        except Exception as errors:
            return SMessages(types="application/zip", error=errors)

#====================================================================

    async def get02(file):
        try:
            from magic import Magic
            mimees = Magic(mime=True)
            mimeos = mimees.from_file(file)
            mimemo = mimeos or "text/plain"
            return SMessages(types=mimemo)
        except Exception as errors:
            return SMessages(types="application/zip", error=errors)

#====================================================================
