from pydantic import BaseModel
from app.blur_video import BlurMethod
from typing import Optional
class BlurVideoRequest(BaseModel):
    key:str
    output_key:str
    blur_method:BlurMethod
class BlurVideoRequestSelective(BaseModel):
    key:str
    output_key:str
    blur_method:BlurMethod
    target_image:str
    
class BlurVideoResponse(BaseModel):
    success:bool
    detail: str|None
    key:str|None
