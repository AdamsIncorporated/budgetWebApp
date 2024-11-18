import base64
from functools import wraps
from flask_login import current_user


def get_current_user_image():
    image_file = None

    if current_user.is_active:
        if current_user.image_file:
            image_file = base64.b64encode(current_user.image_file).decode("utf-8")

    return image_file


def image_wrapper(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Get the current user's image
        kwargs["image_file"] = get_current_user_image()
        return func(*args, **kwargs)

    return decorated_function
