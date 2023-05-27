from app.views.article import generateToken, key_JWT
import jwt
load = {"exemple@exemple.fr": "123"}

def test_checkToken_valid():

    print("Checking valid token")
    encoded = generateToken(load)
    result = jwt.decode(encoded, key_JWT, algorithms=["HS256"])
    print("Resultat: ", result)
    assert result == load