from pydantic import BaseModel
from fastapi import UploadFile

class ProduitSchema(BaseModel):
    id: int
    libelle: str
    description: str
    prix: float
    url_img: UploadFile
    en_promo: bool
    promotion_id: int
    categorie: str
 
class PromotionSchema(BaseModel):
    id: int
    remise: float
    date_deb: str
    date_fin: str

class AdminSchema(BaseModel):
    id: int
    email: str
    password: str