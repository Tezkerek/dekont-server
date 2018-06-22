from django.contrib.auth import get_user_model

def get_username_field():
    """
    Retrieves USERNAME_FIELD from the User model, or "username" if not set
    """
    return getattr(get_user_model(), 'USERNAME_FIELD', "username")
