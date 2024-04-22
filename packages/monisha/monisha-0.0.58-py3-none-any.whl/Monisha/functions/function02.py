from ..scripts import Humon, Scripted
#=============================================================================

def Dbytes(sizes, blank=Scripted.DATA09, second=Scripted.DATA01):
    if not sizes or (sizes == Scripted.DATA02):
        return blank
    nomos = 0
    POWEO = 2**10
    POWER = Humon.DATA01
    while sizes > POWEO:
        sizes /= POWEO
        nomos += 1
    ouing = str(round(sizes, 2)) + Scripted.DATA02 + POWER[nomos] + second
    return ouing

#=============================================================================

def Hbytes(sizes, blank=Scripted.DATA08, second=Scripted.DATA01):
    if not sizes or (sizes == Scripted.DATA02):
        return blank
    nomos = 0
    POWEO = 2**10
    POWER = Humon.DATA02
    while sizes > POWEO:
        sizes /= POWEO
        nomos += 1
    ouing = str(round(sizes, 2)) + Scripted.DATA02 + POWER[nomos] + second
    return ouing

#=============================================================================
