from app.views.article import PDF_to_Bytes, export_pdf
from fastapi.testclient import TestClient
from app.start import app

client = TestClient(app)

def test_bytesToPDF():
    path_PDF = f"https://mercastatic-pdf.s3.amazonaws.com/mercadonaPDF_26-05-2023.pdf"
    value = PDF_to_Bytes(path_PDF)
    assert type(value) == bytes
    assert len(b'value') > 0

def test_route():
    # Envoi d'une requête GET à la route que vous souhaitez tester
    response = client.get("/export-pdf")
    # Vérification du code de statut HTTP
    assert response.status_code == 401