
from verify import verifyPasswordMail
from hash import hashPasswordEmail

def verifyPasswordMail_valid_test():

    print("Test valid ident")
    false_email= "exemple@exemple.fr"
    false_password= "123"
    hashed_email, hashed_password = hashPasswordEmail(false_email,false_password)
    result = verifyPasswordMail(false_email, false_password, hashed_email, hashed_password)
    print("Resultat valid ident: ",result)
    assert result == True

def verifyPasswordMail_invalidMail_test():
    
    print("Test invalidMail")
    false_email= "exemple@exemple.fr"
    false_password= "123"

    hashed_email, hashed_password = hashPasswordEmail(false_email,false_password)

    false_email = "myexemple@exemple.fr"

    result = verifyPasswordMail(false_email, false_password, hashed_email, hashed_password)
    print("Resultat invalid email: ",result)
    assert result == False

def verifyPasswordMail_invalidPassword_test():
    
    print("Test invalidPassword")
    false_email= "exemple@exemple.fr"
    false_password= "123"

    hashed_email, hashed_password = hashPasswordEmail(false_email,false_password)

    false_password = "124"

    result = verifyPasswordMail(false_email, false_password, hashed_email, hashed_password)
    print("Resultat invalid password: ",result)
    assert result == False

verifyPasswordMail_valid_test()
verifyPasswordMail_invalidMail_test()
verifyPasswordMail_invalidPassword_test()