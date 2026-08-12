from uniface.privacy import BlurFace
from enum import Enum

class BlurMethod(Enum):
    PIXELATE = "pixelate"
    GAUSSIAN = "gaussian"
    BLACKOUT = "blackout"
    ELLIPTICAL = "elliptical"
    MEDIAN = "median"
    
    
def getBlurrer(method:BlurMethod):
    print(method)
    return BlurFace(method=method.value)