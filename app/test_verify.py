
from app.verify import verifyPasswordMail
from app.hash import hashPasswordEmail

def test_verifyPasswordMail_valid():

    print("Test valid ident")
    false_email= "exemple@exemple.fr"
    false_password= "123"
    hashed_email, hashed_password = hashPasswordEmail(false_email,false_password)
    result = verifyPasswordMail(false_email, false_password, hashed_email, hashed_password)
    print("Resultat valid ident: ",result)
    assert result == True

def test_verifyPasswordMail_invalidMail():
    
    print("Test invalidMail")
    false_email= "exemple@exemple.fr"
    false_password= "123"

    hashed_email, hashed_password = hashPasswordEmail(false_email,false_password)

    false_email = "myexemple@exemple.fr"

    result = verifyPasswordMail(false_email, false_password, hashed_email, hashed_password)
    print("Resultat invalid email: ",result)
    assert result == False

def test_verifyPasswordMail_invalidPassword():
    
    print("Test invalidPassword")
    false_email= "exemple@exemple.fr"
    false_password= "123"

    hashed_email, hashed_password = hashPasswordEmail(false_email,false_password)

    false_password = "124"

    result = verifyPasswordMail(false_email, false_password, hashed_email, hashed_password)
    print("Resultat invalid password: ",result)
    assert result == False
