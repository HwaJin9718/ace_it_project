from fastapi import Depends, APIRouter, BackgroundTasks
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema

from schema.request import EmailSchema

router = APIRouter(prefix="/inquiry")

conf = ConnectionConfig(
    MAIL_USERNAME="ajffhsk2248@naver.com", # 보내는 사람 이메일
    MAIL_PASSWORD="1234", # 보내는 사람 계정 비밀번호
    MAIL_FROM="ajffhsk2248@naver.com", # 보내는 사람 이메일
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
    return {"message": "Mail sent successfully"}

