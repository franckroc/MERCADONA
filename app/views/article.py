from fastapi import APIRouter, Request, HTTPException, status, Form, UploadFile, File
from fastapi.responses import RedirectResponse

from app.models.article import Produit, Admin, Promotion
from app.core.myconfig import templates

# importe fonction custom de vérification mail et password en bdd
from app.verify import verifyPasswordMail

# importe fonction custom de prévention SQL injection
from app.sqli import sql_i_injection

#librairie pour générer et vérifier token
import jwt  
from decouple import config

#####################################################
##### class adminLogin pour sauvegarde token ########

class adminLogin:
    admin_token: str = None
#####################################################

homePage = APIRouter()       # route public
articlesViews = APIRouter()  # route public
adminConnect = APIRouter()   # route public
backOffice = APIRouter()     # route privé

######## fonctions générateur et verif token ########

key: str = config("JWT_SECRETKEY")

def generateToken(payload: dict) ->str:
    encoded = jwt.encode(payload, key, algorithm="HS256")
    return encoded

def checkToken(token: str) -> bool:
    try:
        jwt.decode(token, key, algorithms="HS256")
        return True
    
    except (jwt.InvalidKeyError, jwt.InvalidSignatureError, 
            jwt.InvalidTokenError, jwt.InvalidAlgorithmError):
        return False

def validToken():
    if checkToken(adminLogin.admin_token) != True:
        raise HTTPException(status_code=405, detail="Accès non autorisé")
    
#################### type hints ####################

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

@articlesViews.get("/articles/", tags=["articles"])
async def articles_list(request: Request, filter: str = "libelle"):
    
    # afficher les produits selon le filtre sélectionné - par défaut filter="libelle"
    match filter:

        case "libelle":
            # requetes avec jointure sur tables produit et promotion
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

###############################################
####### routes formulaire connexion ###########

#################### route GET #######################

@adminConnect.get("/admin/", tags=["admin"])
async def admin(request: Request):

    return templates.TemplateResponse("form_admin.html", {"request": request})

#################### route POST #######################

@adminConnect.post("/dataForm/", tags=["admin"]) 
async def login(email: str = Form(...), password: str = Form(...)):

    # verifiction SQLi 
    nosqli = sql_i_injection(email)
    if nosqli:
        nosqli = sql_i_injection(password)
        if nosqli:
            # si pas d'injections repérées requete BDD pour récupérér les données admin
            users = await Admin.all()
        else:
            # sinon redirection page d'accueil
            return RedirectResponse(url="/", status_code=status.HTTP_205_RESET_CONTENT)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_205_RESET_CONTENT)

    # recherche parmi les données admin
    for user in users:   
        # verif concordances email et password du formulaire / email et password haché salé en BDD
        valid = verifyPasswordMail(email, password, user.mail, user.password)

        ##### réponse si identifiants valides
        if valid == True:

            # génération token d'authentification
            payload= {f"{email}":f"{password}"}
            token = generateToken(payload)

            # sauvegarde du token dans la classe adminLogin
            adminLogin.admin_token = token

            # redirection vers route protégée /BOffice
            return RedirectResponse(url='/BOffice/', status_code=status.HTTP_303_SEE_OTHER)
        else:
            # sinon retour accueil
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

########################################################
################# routes BackOffice ####################

#############  route GET page d'accueil du Back Office ###############

@backOffice.get("/BOffice/", tags=["backOffice"])
async def adminBackOffice(request: Request):

    #vérification du token 
    validToken()

    return templates.TemplateResponse( "Boffice.html", { "request": request})

########### route post createProd (création produit) ######################

@backOffice.post("/createProd/", tags=["backOffice"])
async def createProd(request: Request, label: str = Form(...), description: str = Form(...),
                     price: float = Form(...), promo: str = Form(...), 
                     images: UploadFile = File(...) , categorie: str = Form(...)):
    
    # vérification token
    validToken()

    # transforme la valeur du bouton radio en_promo en booléen
    if promo == "on":
        promo = True
    else:
        promo = False

    # téléversement du fichier image (chemin absolu) dans le dossier de destination  
    file_path = f"C:/Users/kiki/Desktop/mercadona/public/img/{images.filename}" 

    with open(file_path, "wb") as buffer:
        buffer.write(await images.read())

    # récomposition chemin relatif de l'image pour BDD
    path = f"public/img/{images.filename}"

    #composition de l'article et enregistrement dans la table Produit
    article = Produit(libelle=label.capitalize(), description=description, prix=price, 
                      url_img=path, en_promo=promo, categorie=categorie.lower())
    
    await article.save()

    return templates.TemplateResponse(
        "article_create.html",
        {
            "request": request,
            "id": article.id,
            "libelle": article.libelle,
            "description": article.description,
            "prix": article.prix,
            "categorie": article.categorie,
            "promotion": article.en_promo
        })

####################################################################################
######### route post createPromo (création promo et mise à jour produit) ###########

@backOffice.post("/createPromo/", tags=["backOffice"])
async def createPromo(id_produit: int = Form(...), dateD: str = Form(...),
                      dateF: str = Form(...), remise: int = Form(...)):

    # vérification token
    validToken()

    # composition de la promotion et enregistrement
    promotion = Promotion(remise=remise, date_deb=dateD, date_fin=dateF)
    await promotion.save()

    # mise a jour du produit sélectionné avec la promotion
    article = await Produit.get(id=id_produit)
    article.promotion_id = promotion.id
    article.en_promo = True
    await article.save()

    return {"message" : f"La promotion ID: {promotion.id} est crée pour l'article: {article.id}"}