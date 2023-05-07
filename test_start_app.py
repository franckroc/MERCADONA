from fastapi.testclient import TestClient

from start import app 

################################## start ##########################

client = TestClient(app)

def root_test():
    response = client.get("/")
    assert response.status_code == 200