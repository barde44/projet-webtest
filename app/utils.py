import re

def is_valid_email(email: str) -> bool:
    """
    Vérifie si l'adresse email est valide selon un pattern simple.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None
