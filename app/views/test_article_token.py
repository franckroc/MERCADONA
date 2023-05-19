from app.views.article import generateToken, key
import jwt
load = {"exemple@exemple.fr":"123"}

def test_checkToken_invalid():

    print("Checking invalid token")
    encoded = generateToken(load)
    result = jwt.decode(encoded+"a", key, algorythms=["HS256"])
    print("Resultat: ", result)
    assert result == False

def test_checkToken_valid():

    print("Checking valid token")
    encoded = generateToken(load)
    result = jwt.decode(encoded, key, algorithms=["HS256"])
    print("Resultat: ", result)
    assert result == True