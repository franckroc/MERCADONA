from fastapi import APIRouter, Request, HTTPException, status, Form
from fastapi.responses import RedirectResponse

from app.models.article import Produit, Admin, Promotion
from app.core.config import templates

# importe fonction de vérification mail et password
from app.verify import verifyPasswordMail
# importe fonction prévention SQLi
from app.sqli import sql_i_injection

from time import sleep 
import jwt  

########################################
########### admin data #################

class adminLogin:
    admin_token: str = None

################## START ###############

homePage = APIRouter()  # route public
articlesViews = APIRouter()  # route public
adminConnect = APIRouter() # route public
backOffice = APIRouter()   # route privé

##### fonctions générateur et verif token ####

def generateToken(payload: dict) ->str:
    key = "secret"
    encoded = jwt.encode(payload, key, algorithm="HS256")
    return encoded

def checkToken(token: str) -> bool:
    key = "secret"

    try:
        jwt.decode(token, key, algorithms="HS256")
        return True
    
    except (jwt.InvalidKeyError, jwt.InvalidSignatureError, 
            jwt.InvalidTokenError, jwt.InvalidAlgorithmError):
        return False

#### fonction de validation du token ######

def validToken():
    if checkToken(adminLogin.admin_token) != True:
        raise HTTPException(status_code=405, detail="Accès non autorisé")
    
############### type hints ################

valid: bool
email: str
password: str
user: str
nosqli: bool

######################################################
############ route GET / Page d'accueil ##############

@homePage.get("/", tags=["home"])
async def root(request: Request):  
    adminLogin.admin_token = None

    return templates.TemplateResponse("index.html", { "request": request })

######################################################
############### route GET /articles ##################

@articlesViews.get("/articles", tags=["articles"])
async def articles_list(request: Request, filter: str = "libelle"):
    
    # afficher les produits selon le filtre sélectionné
    match filter:

        case "libelle":
            produits = await Produit.all().prefetch_related('promotion').order_by(filter)
        case _:
            produits = await Produit.filter(categorie=filter).prefetch_related('promotion')
   
    # les variables produits et filtre sont passées au template
    return templates.TemplateResponse(
        "products_list.html",
        {
            "request": request,
            "produits": produits,
            "filtre": filter
        })

######################################################
####### routes /admin formulaire connexion ###########

#################### route GET #######################

@adminConnect.get("/admin/", tags=["admin"])
async def admin(request: Request):

    return templates.TemplateResponse("form_admin.html", {"request": request})

#################### route POST #######################

@adminConnect.post("/dataForm/", tags=["admin"]) 
async def login(email: str = Form(...), password: str = Form(...)):

    # verif SQLi 
    nosqli = sql_i_injection(email)
    if nosqli:
        nosqli = sql_i_injection(password)
        if nosqli:
            # requete BDD pour récupérér data(s) admin(s)
            users = await Admin.all()
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_205_RESET_CONTENT)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_205_RESET_CONTENT)

    # recherche parmi les data(s) admin(s)
    for user in users:   
        # verif concordances email et password du formulaire / email et password haché salé en BDD
        valid = verifyPasswordMail(email, password, user.mail, user.password)

        ##### réponse si identifiants valides
        if valid == True:

            # génération token d'authentification
            payload= {f"{email}":f"{password}"}
            token = generateToken(payload)

            # safe data admin login
            adminLogin.admin_token = token

            # redirection vers route protégée
            return RedirectResponse(url='/BOffice/', status_code=status.HTTP_303_SEE_OTHER)
        else:
            # sinon retour accueil
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

########################################################
################# routes BackOffice ####################

#############  route GET page d'accueil  ###############

@backOffice.get("/BOffice/", tags=["backOffice"])
async def adminBackOffice(request: Request):

    validToken()

    return templates.TemplateResponse( "Boffice.html", { "request": request})

########### route post createProd ######################

@backOffice.post("/createProd/", tags=["backOffice"])
async def createProd(label: str = Form(...), description: str = Form(...),
                     price: float = Form(...), promo: str = Form(...), 
                     images: list = Form(...), categorie: str = Form(...)):
    
    validToken()

    # transforme valeur bouton radio en booléen
    if promo == "on":
        promo = True
    else:
        promo = False

    # recompose path image
    path = f"public/img/{images[0]}"

    #composition de l'article et enregistrement dans la table Produit
    article = Produit(libelle=label.capitalize(), description=description, prix=price, 
                      url_img=path, en_promo=promo, categorie=categorie.lower())
    await article.save()

    return {"message":f"Le produit ID: {article.id} est crée"}

@backOffice.post("/createPromo/", tags=["backOffice"])
async def createPromo(id_produit: int = Form(...), dateD: str = Form(...),
                      dateF: str = Form(...), remise: int = Form(...)):

    validToken()

    # composition de la promotion et enregistrement
    promotion = Promotion(remise=remise, date_deb=dateD, date_fin=dateF)
    await promotion.save()

    # mise a jour du produit sélectionné avec la promotion
    article = await Produit.get(id=id_produit)
    article.promotion_id = promotion.id
    article.en_promo = True
    await article.save()

    return {"message" : f"La promotion ID: {promotion.id} est crée"}