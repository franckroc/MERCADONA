from article import generateToken, checkToken

def checkToken_invalid_test(load):

    print("Checking invalid token")
    encoded = generateToken(load)
    result = checkToken(encoded + "1")
    print("Resultat: ", result)
    assert result == False

def checkToken_valid_test(load):

    print("Checking valid token")
    encoded = generateToken(load)
    result = checkToken(encoded)
    print("Resultat: ", result)
    assert result == True

payload = {"exemple@exemple.fr":"123"}
checkToken_valid_test(payload)
checkToken_invalid_test(payload)
