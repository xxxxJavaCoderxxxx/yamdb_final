from api_yamdb.settings import EMAIL_HOST_USER
from core.models import CustomUserManager, User


def send_email(user: User):
    """Отправить письмо для user."""
    confirmation_code = CustomUserManager().make_random_password()
    user.email_user(
        subject='Confirmation code',
        message=f'Hello {user.username}! '
                f'Your confirmation code: {confirmation_code}',
        from_email=EMAIL_HOST_USER,
    )
    user.set_password(confirmation_code)
    user.confirmation_code = True
    user.save()
    return user
