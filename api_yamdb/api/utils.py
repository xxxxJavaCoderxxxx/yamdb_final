from core.models import CustomUserManager, User


def send_email(user: User):
    """Отправить письмо для user."""
    confirmation_code = CustomUserManager().make_random_password()
    user.email_user(
        subject='Confirmation code',
        message=f'Hello {user.username}! '
                f'Your confirmation code: {confirmation_code}',
        from_email='noreply@api_yamdb.ru',
    )
    user.set_password(confirmation_code)
    user.confirmation_code = True
    user.save()
    return user
