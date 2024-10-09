from fastapi import Depends, APIRouter, BackgroundTasks
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema

from schema.request import CreateInquiryRequest, EmailSchema

router = APIRouter(prefix="/inquiry")

conf = ConnectionConfig(
    MAIL_USERNAME="ajffhsk2248@naver.com", # 보내는 사람 이메일
    MAIL_PASSWORD="hjsong059718**",
    MAIL_FROM="ajffhsk2248@naver.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.naver.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

@router.post("")
def send_inquiry(
        email: EmailSchema,
        background_tasks: BackgroundTasks
):

    body = (
        f"문의 작성자: {email.message.inquiry_writer}\n"
        f"작성자 이메일: {email.message.inquiry_writer_email or '없음'}\n"
        f"작성자 연락처: {email.message.inquiry_writer_contact_number or '없음'}\n"
        f"문의 내용: {email.message.inquiry_details or '없음'}"
    )

    message = MessageSchema(
        subject=email.subject,
        recipients=[email.email],
        body=body,
        subtype='plain'
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
    return {"message": "email has been sent"}

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
