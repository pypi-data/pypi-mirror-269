from magic import Magic
#====================================================================

def filestype(file):
    try: 
        mimees = Magic(mime=True)
        mimeos = mimees.from_file(file)
        mimemo = mimeos or "text/plain"
        return mimemo
    except Exception:
        mimemo = "application/zip"
        return mimemo

#====================================================================

async def filextype(file):
    try: 
        mimees = Magic(mime=True)
        mimeos = mimees.from_file(file)
        mimemo = mimeos or "text/plain"
        return mimemo
    except Exception:
        mimemo = "application/zip"
        return mimemo

#====================================================================
