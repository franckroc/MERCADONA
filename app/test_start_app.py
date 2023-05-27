from fastapi.testclient import TestClient
from app.start import app 
import unittest
class TestSomeGet_Endpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/")
        assert response.status_code == 200

    def test_admin(self):
        response = self.client.get("/admin")
        assert response.status_code == 200

    def test_adminBackOffice(self):
        response = self.client.get("/BOffice")
        assert response.status_code == 401
