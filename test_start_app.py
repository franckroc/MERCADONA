from fastapi.testclient import TestClient
from start import app 

client = TestClient(app)

def root_test():

    print("Test app")
    response = client.get("/")
    print("Status response: ",response.status_code)
    assert response.status_code == 200

root_test()