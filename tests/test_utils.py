from app.utils import is_valid_email

def test_valid_email():
    assert is_valid_email("test@example.com") == True
    assert is_valid_email("user.name@domain.co") == True

def test_invalid_email():
    assert is_valid_email("invalid-email") == False
    assert is_valid_email("user@.com") == False
    assert is_valid_email("user@domain") == False
