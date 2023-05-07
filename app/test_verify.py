
from app.verify import verifyPasswordMail
from app.hash import hashPasswordEmail

def verifyPasswordMail_test():
    
    false_email= "exemple@exemple.fr"
    false_password= "123"

    hashed_email, hashed_password = hashPasswordEmail(false_email,false_password)

    result = verifyPasswordMail(false_email, false_password, hashed_email, hashed_password)

    assert result == True