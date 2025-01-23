from pydantic import BaseModel

class CheckImeiResponse(BaseModel):
    deviceName : str
    imei : str
    modelName : str
    brand : str
    manufacturer : str

class BasicResponse(BaseModel):
    is_succeeded : bool
    additional_info : str

class CheckImeiBody(BaseModel):
    imei : str
    token : str

class AddUserBody(BaseModel):
    telegram_id : int
    token : str