from typing import Optional

from pydantic import BaseModel, field_validator, Field


def luhn_check(imei: str) -> bool:
    if len(imei) != 15 or not imei.isdigit():
        return False
    total = 0
    for i, char in enumerate(imei):
        digit = int(char)
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit = digit - 9
        total += digit
    return total % 10 == 0


class AdditionalInfo(BaseModel):
    deviceName: Optional[str] = None
    image: Optional[str] = None
    imei: Optional[str] = None
    estPurchaseDate: Optional[int] = None
    simLock: Optional[bool] = None
    warrantyStatus: Optional[str] = None
    repairCoverage: Optional[str] = None
    technicalSupport: Optional[str] = None
    modelDesc: Optional[str] = None
    demoUnit: Optional[bool] = None
    refurbished: Optional[bool] = None
    purchaseCountry: Optional[str] = None
    apple_region: Optional[str] = Field(
        None, alias="apple/region"
    )  # Используем псевдоним для поля с "/"
    fmiOn: Optional[bool] = None
    lostMode: Optional[str] = None
    usaBlockStatus: Optional[str] = None
    network: Optional[str] = None

    class Config:
        extra = "allow"


class CheckImeiResponse(BaseModel):
    is_succeeded: bool
    additional_info: Optional[AdditionalInfo] = None | str


class BasicResponse(BaseModel):
    is_succeeded: bool
    additional_info: str


class CheckImeiBody(BaseModel):
    imei: str
    token: str

    @field_validator("imei")
    def validate_imei(cls, v):
        if not v.isdigit() or len(v) != 15:
            raise ValueError("IMEI must be a 15-digit number")
        if not luhn_check(v):
            raise ValueError("Invalid IMEI (failed Luhn check)")
        return v


class AddUserBody(BaseModel):
    telegram_id: int
    token: str
