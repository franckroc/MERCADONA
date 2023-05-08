from app.views.article import generateToken, checkToken
load = {"exemple@exemple.fr":"123"}

def test_checkToken_invalid():

    print("Checking invalid token")
    encoded = generateToken(load)
    result = checkToken(encoded + "1")
    print("Resultat: ", result)
    assert result == False

def test_checkToken_valid():

    print("Checking valid token")
    encoded = generateToken(load)
    result = checkToken(encoded)
    print("Resultat: ", result)
    assert result == True

