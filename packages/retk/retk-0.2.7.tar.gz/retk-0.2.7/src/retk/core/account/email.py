import email.header
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from textwrap import dedent
from typing import List, Tuple

import jwt

from retk import const, config, regex, utils
from retk.core import async_task


class EmailServer:
    default_language = const.Language.EN

    lang_subject = {
        const.Language.EN.value: "Rethink: Security Code",
        const.Language.ZH.value: "Rethink: 安全密码",
    }
    lang_content = {
        const.Language.EN.value: dedent("""\
        Please use the following security code for your Rethink account {email}:
        <br><br>
        Security Code: <br><br>
        <strong style="font-size:26px;">{numbers}</strong>
        <br><br>
        Valid for {expire} minutes, please do not tell others to prevent personal information leakage.
        <br><br>
        If you did not request this code, you can safely ignore this email, \
        someone may have entered your email address by mistake.
        <br><br>
        Thank you!<br>
        Rethink Team
        """),
        const.Language.ZH.value: dedent("""\
        请使用以下用于 Rethink 账户 {email} 的安全代码：
        <br><br>
        安全代码：<br><br>
        <strong style="font-size:26px;">{numbers}</strong>
        <br><br>
        有效期 {expire} 分钟，请勿告知他人，以防个人信息泄露。
        <br><br>
        若您并未要求此代码，可以安全地忽视此邮件，可能有人误输入了您的电子邮件地址。
        <br><br>
        谢谢！<br>
        Rethink 团队
        """),
    }

    def get_subject_content(self, recipient: str, numbers: str, expire: int, language: str) -> Tuple[str, str]:
        try:
            subject = self.lang_subject[language]
            content_temp = self.lang_content[language]
        except KeyError:
            subject = self.lang_subject[self.default_language]
            content_temp = self.lang_content[self.default_language]
        content = content_temp.format(email=utils.mask_email(recipient), numbers=numbers, expire=expire)
        return subject, content

    def send(self, recipient: str, numbers: str, expire: int, language: str) -> const.Code:
        subject, content = self.get_subject_content(
            recipient=recipient, numbers=numbers, expire=expire, language=language
        )

        return self._send(
            subject=subject,
            recipients=[recipient],
            html_message=content
        )

    @staticmethod
    def email_ok(email_addr: str) -> bool:
        if regex.EMAIL.fullmatch(email_addr) is None:
            return False
        return True

    def _send(self, recipients: List[str], subject: str, html_message: str) -> const.Code:
        for recipient in recipients:
            if not self.email_ok(recipient):
                return const.Code.INVALID_EMAIL
        conf = config.get_settings()
        msg = MIMEMultipart('alternative')
        msg['Subject'] = email.header.Header(subject, 'utf-8')
        msg['From'] = conf.RETHINK_EMAIL
        msg['To'] = ", ".join(recipients)
        html_body = MIMEText(html_message, 'html', 'utf-8')
        msg.attach(html_body)

        async_task.put_task(
            task_name=async_task.TaskName.SEND_EMAIL,
            recipients=recipients,
            subject=msg.as_string()
        )
        return const.Code.OK


email_server = EmailServer()


def encode_number(number: str, expired_min: int) -> str:
    token = utils.jwt_encode(
        exp_delta=timedelta(minutes=expired_min),
        data={"code": number + config.get_settings().CAPTCHA_SALT}
    )
    return token


def verify_number(token: str, number_str: str) -> const.Code:
    code = const.Code.CAPTCHA_ERROR
    try:
        data = utils.jwt_decode(token)
        if data["code"] == number_str + config.get_settings().CAPTCHA_SALT:
            code = const.Code.OK
    except jwt.ExpiredSignatureError:
        code = const.Code.CAPTCHA_EXPIRED
    except (jwt.DecodeError, Exception):
        code = const.Code.INVALID_AUTH
    return code
