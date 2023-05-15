import bcrypt

############ Fonction hachage et sel Bcrypt password et mail ##########

def hashPasswordEmail(email:str, password: str) ->str:

    # Convertion bytes
    password_bytes: bytes = password.encode('utf-8')
    email_bytes: bytes = email.encode('utf-8')

    # génération sel
    salt: bytes = bcrypt.gensalt()

    # Hash et sel
    hashed_password: bytes = bcrypt.hashpw(password_bytes, salt)
    hashed_email: bytes = bcrypt.hashpw(email_bytes, salt)

    # Retour hash/sel paswword et email
    return  hashed_email.decode('utf-8'), hashed_password.decode('utf-8')