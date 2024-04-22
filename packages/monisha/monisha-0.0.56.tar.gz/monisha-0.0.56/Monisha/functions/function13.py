import random
from ..scripts import Strine, Scripted
#=======================================================================================

async def ransig():
    raumes = random.randint(10, 32)
    ouoing = Scripted.DATA01.join(random.choice(Strine.DATA04) for _ in range(raumes))
    return ouoing

#=======================================================================================
