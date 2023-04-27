import bcrypt

############# fonction de verif des infos de connexion ############

def verifyPasswordMail(email: str, password: str, hashed_email: str, hashed_password: str) -> bool:

    # Convertion bytes
    password_bytes = password.encode('utf-8')
    email_bytes = email.encode('utf-8')

    # vérification
    is_email_valid: bool = bcrypt.checkpw(email_bytes, hashed_email.encode('utf-8'))
    is_password_valid: bool = bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))

    # Return True si password et mail valide sinon False
    return is_password_valid and is_email_valid