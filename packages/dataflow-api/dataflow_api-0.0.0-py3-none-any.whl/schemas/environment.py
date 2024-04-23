"""schemas/environment.py"""
from pydantic import BaseModel



class Environment(BaseModel):
    """
    Base Model Environment
    """

    id:int
    url:str = None
    name:str
    short_name:str
    enabled:bool=True
    version:str = None
    is_latest:bool=True
    base_image_id:int
    short_name:str
    status:str
    icon:str=None
    py_version:str = None
    r_version:str= None
    py_requirements:str = None
    r_requirements:str =None
    py_requirements_compiled:str = None
    r_requirements_compiled:str= None



class ShowEnvironment(BaseModel):
    """
    Base Model ShowEnvironment py_requirements
    """

    py_requirements:str =None

    class Config():
        """setting orm_mode"""
        from_attributes=True



class Compile(BaseModel):
    """
    Pip Compile
    """

    image_id:int
    requirements_in:str=None
