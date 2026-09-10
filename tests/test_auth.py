import bcrypt
from frontend.auth import validate_email, validate_password_complexity

def test_validate_email():
    assert validate_email("pradeepthi297@gmail.com") is True
    assert validate_email("invalid_email") is False

def test_validate_password_complexity():
    assert validate_password_complexity("password123") is True
    assert validate_password_complexity("123") is False

def test_password_hashing():
    password = "secret_password"
    salt = bcrypt.gensalt()
    pwd_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    assert bcrypt.checkpw(password.encode('utf-8'), pwd_hash)