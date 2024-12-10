def is_password_complex(password):
    if len(password) < 12 or len(password) > 16:
        return False

    has_lowercase = False
    has_uppercase = False
    has_digit = False
    has_special_char = False

    for char in password:
        if char.islower():
            has_lowercase = True
        elif char.isupper():
            has_uppercase = True
        elif char.isdigit():
            has_digit = True
        elif char in "@$!%*?&":
            has_special_char = True

    return has_lowercase and has_uppercase and has_digit and has_special_char
