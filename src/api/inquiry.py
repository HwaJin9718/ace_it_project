from fastapi import Depends, APIRouter
from fastapi_mail import ConnectionConfig

from schema.request import CreateInquiryRequest

router = APIRouter(prefix="/inquiry")

conf = ConnectionConfig(
    MAIL_USERNAME="<EMAIL>",
    MAIL_PASSWORD="<PASSWORD>",
    MAIL_FROM="<EMAIL>",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

# @router.post("")
# def send_inquiry(
#         request: CreateInquiryRequest
# ):

# @router.get("", status_code=200)
# def get_inquiry(
#         inquiry_repo: InquiryRepository = Depends()
# ):
#     inquiry: List[Inquiry] = inquiry_repo.get_inquiry()
#
#     return inquiry
#
# @router.get("/{inquiry_id}", status_code=200)
# def get_inquiry(
#         inquiry_id: int,
#         inquiry_repo: InquiryRepository = Depends()
# ):
#     inquiry: Inquiry = inquiry_repo.get_inquiry_by_id(inquiry_id)
#
#     if inquiry:
#         return inquiry
#
#     raise HTTPException(status_code=404, detail="Inquiry Not Found")
