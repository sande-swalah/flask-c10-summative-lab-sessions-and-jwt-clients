def validate_username_value(username):
    if not username or not username.strip():
        raise ValueError("Username is required")
    return username.strip()
