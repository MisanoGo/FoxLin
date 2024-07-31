from typing import  Any
import string,random

from pydantic import BaseModel as BsMdl

class BaseModel(BsMdl):
    class Config:
        arbitrary_types_allowed = True
        
def get_attr(obj, name) -> Any:
    return object.__getattribute__(obj, name)

def generate_random_name(length: int = 8) -> str:
    """Generate a random session name."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
