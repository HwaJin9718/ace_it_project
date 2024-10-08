from datetime import date
from typing import Optional, Dict

from pydantic import BaseModel


class CreateInfoRequest(BaseModel):
    information_name: str
    information_content: str


class CreateHistoryRequest(BaseModel):
    history_section_code: int
    history_date: date
    history_content: str


# 이미지 업로드는 잠시 보류!!
class CreateBusinessClientRequest(BaseModel):
    client_name: str
    # client_logo_name: str


class CreateCompanyVisionValuesRequest(BaseModel):
    vv_name: str
    vv_content: Optional[str] = None
    vv_details: Optional[Dict] = None


class CreateBusinessAreaRequest(BaseModel):
    area_name: str
    area_type: Optional[Dict] = None
    area_content: Optional[str] = None
    area_details: Optional[Dict] = None


# 받은 데이터 특정 이메일로 발송 필요!
class CreateInquiryRequest(BaseModel):
    inquiry_writer: str
    inquiry_writer_email: Optional[str] = None
    inquiry_writer_contack_number: Optional[str] = None
    inquiry_details: Optional[str] = None
