from app.views.article import PDF_to_Bytes, export_pdf
from fastapi.testclient import TestClient
from app.start import app

client = TestClient(app)

def test_route():
    # Envoi d'une requête GET à la route que vous souhaitez tester
    response = client.get("/export-pdf")
    # Vérification du code de statut HTTP
    assert response.status_code == 401
    
def test_bytesToPDF():
    path_PDF = "https://mercapdf.s3.eu-west-3.amazonaws.com/mercadonaPDF_29-05-2023.pdf"
    value = PDF_to_Bytes(path_PDF)
    assert type(value) == bytes
    assert len(b'value') > 0