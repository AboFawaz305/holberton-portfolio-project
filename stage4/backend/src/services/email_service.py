"""Email service using Resend
"""


import jwt
import resend
from constants import (RESEND_API_KEY, FRONTEND_URL,
                       FROM_EMAIL, SECRET_KEY, ALGORITHM)


resend.api_key = RESEND_API_KEY


def generate_verification_token(email):
    """Generate a JWT token containing the email"""
    return jwt.encode({"email": email}, SECRET_KEY, algorithm=ALGORITHM)


def decode_verification_token(token):
    """Decode the verification token and return the email"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("email")
    # pylint: disable=broad-exception-caught
    except Exception:
        return None


def send_verification_email(to_email, token, username):
    """Send verification email to user"""
    verification_link = f"{FRONTEND_URL}/verify-email/{token}"

    try:
        resend. Emails.send({
            "from": FROM_EMAIL,
            "to": to_email,
            "subject":  "تأكيد البريد الإلكتروني - Verify Your Email",
            "html": f"""
            <div dir="rtl" style="font-family: Arial, sans-serif;
            max-width:  600px; margin: 0 auto;">
                <h2>مرحباً {username}!</h2>
                <p>شكراً لتسجيلك معنا.
                  يرجى تأكيد بريدك الإلكتروني بالنقر على الزر أدناه: </p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_link}"
                       style="background-color: #4CAF50;
                       color: white; padding: 15px 30px;
                              text-decoration: none;
                              border-radius: 5px; font-size: 16px;">
                        تأكيد البريد الإلكتروني
                    </a>
                </div>
            </div>
            """
        })
        return True
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(f"Failed to send verification email: {e}")
        return False
