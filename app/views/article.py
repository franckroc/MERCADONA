from fastapi import APIRouter, Request, HTTPException, status, Form, UploadFile, File
from fastapi.responses import RedirectResponse

from app.models.article import Produit, Admin, Promotion, Categorie
from app.core.myconfig import templates, S3
# importe fonction custom de vérification mail et password en bdd
from app.verify import verifyPasswordMail
# importe fonction custom de prévention SQL injection
from app.sqli import sql_i_injection

#librairie pour générer et vérifier token
import jwt  

from decouple import config
# librarie gestion erreur ORM Tortoise
from tortoise.exceptions import DoesNotExist

#####################################################
##### class adminLogin pour sauvegarde token ########
class adminLogin:
    admin_token: str = ""
    
#####################################################

homePage = APIRouter()       # route public
articlesViews = APIRouter()  # route public
adminConnect = APIRouter()   # route public
backOffice = APIRouter()     # route privé

######## fonctions générateur et verification token ########

key: str = config("JWT_SECRETKEY")

def generateToken(payload: dict) ->str:
    encoded = jwt.encode(payload, key, algorithm="HS256")
    return encoded

def checkToken(token: str) -> bool:
    try:
        jwt.decode(token, key, algorithms=["HS256"])
        return True
    
    except (jwt.InvalidKeyError, jwt.InvalidSignatureError, 
            jwt.InvalidTokenError, jwt.InvalidAlgorithmError):
        return False

def validToken():
    if checkToken(adminLogin.admin_token) != True:
        raise HTTPException(status_code=405, detail="MERCADONA - Accès non autorisé")

#################### type hints ####################

valid: bool
email: str
password: str
user: str
nosqli: bool

######################################################
############ route GET / Page d'accueil ##############
######## template:  index.html   #####################

@homePage.get("/", tags=["home"])
async def root(request: Request): 

    # efface le token
    adminLogin.admin_token = ""

    return templates.TemplateResponse("index.html", { "request": request })

######################################################
############### route GET /articles ##################
########## Template products_list.html ###############

@articlesViews.get("/articles/", tags=["articles"])

# par défaut filter = "libellé" --> tous les articles
async def articles_list(request: Request, filter: str = "libelle"):

    # récupération de toutes les catégories en BDD pour liste déroulante
    categories = await Categorie.all()
    # capture du filtre pour message CATEGORIE
    libelleCategorie = filter

    # afficher les produits selon le filtre sélectionné
    match filter:

        case "libelle":
            # requetes avec jointure sur tables produit , promotion et categorie
            produits = await Produit.all().prefetch_related('promotion', 'categorie')
        case _:
            produits = await Produit.filter(categorie=filter).prefetch_related('promotion', 'categorie')
            # récupération du nouveau libellé catégorie pour message CATEGORIE
            libelleCategorie = await Categorie.filter(id=filter)
        
    # les variables produits, categories, filtre et libelleCategorie sont passées au template
    return templates.TemplateResponse(
        "products_list.html",
        {
            "request": request,
            "produits": produits,
            "categories": categories,
            "libelleCategorie": libelleCategorie,
            "filtre": filter
        })

###############################################
####### routes formulaire connexion ###########
####### Template: form_admin.html   ###########

#################### route GET ################

@adminConnect.get("/admin/", tags=["admin"])
async def admin(request: Request):

    return templates.TemplateResponse("form_admin.html", {"request": request})

#################### route POST ###############

@adminConnect.post("/dataForm/", tags=["admin"]) 

# récupération email et password du formulaire
async def login(email: str = Form(...), password: str = Form(...)):

    # verification SQLi sur email et password --> fonction (sqli.py)
    nosqli = sql_i_injection(email)
    if nosqli == False:
        nosqli = sql_i_injection(password)
        if nosqli == False:
            # si pas d'injections repérées requete BDD pour récupérér les données admin
            users = await Admin.all()  #1 haché/salé email puis users = await Admin.get(mail=email_hashed)
        else:
            # sinon redirection page d'accueil
            return RedirectResponse(url="/", status_code=status.HTTP_205_RESET_CONTENT)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_205_RESET_CONTENT)

    # recherche parmi les données admin (1 seul admin)
    # si plusieurs admin modif #1
    for user in users:   
        # fonction (verify.py) verification email et password du formulaire avec BDD
        valid = verifyPasswordMail(email, password, user.mail, user.password)

        ##### réponse si identifiants valides
        if valid == True:

            # génération token d'authentification avec email/password du formulaire
            payload= {f"{email}":f"{password}"}
            token = generateToken(payload)
            # sauvegarde du token dans la classe adminLogin
            adminLogin.admin_token = token
            # redirection vers route protégée /BOffice
            return RedirectResponse(url='/BOffice/', status_code=status.HTTP_303_SEE_OTHER)
        
        # sinon retour accueil
        else:
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

########################################################
################# routes BackOffice ####################
############ Template: Boffice.html  ###################

########  route GET page d'accueil du Back Office ######

@backOffice.get("/BOffice/", tags=["backOffice"])
async def adminBackOffice(request: Request):

    #vérification du token. Si invalide code 405 Accès non autorisé 
    validToken()

    return templates.TemplateResponse( "Boffice.html", { "request": request })

####### route post createProd (création produit) ########
######## Template: article_create.html ##################

@backOffice.post("/createProd/", tags=["backOffice"])

# récupération des données formulaire création produit
# catégorie est le libellé catégorie
async def createProd(request: Request, label: str = Form(...), description: str = Form(...),
                     price: float = Form(...), promo: str = Form(...), 
                     images: UploadFile = File(...) , categorie: str = Form(...)):
    
    # vérification token
    validToken()

    # transforme la valeur str du bouton radio en booléen
    if promo == "on":
        promo = True
    else:
        promo = False

    '''
    # téléversement du fichier image dans le dossier de destination local
    with open(path, "wb") as buffer:
        buffer.write(await images.read())
    '''

    try:
        # récupération de l'id de la catégorie donnée
        cat = await Categorie.get(categorie=categorie)  #.values('id')
        idCat = cat.id 
    # si nouvelle catégorie - création catégorie et récupération de son id
    except DoesNotExist:
        cat = Categorie(categorie=categorie)
        await cat.save()
        idCat = cat.id

    # téléversement du fichier image à partir du répertoire local au bucket s3
    S3.s3_client.upload_fileobj(images.file, S3.bucket_name, images.filename)

    #composition de l'article et enregistrement dans la table avec l'id catégorie
    article = Produit(libelle=label.capitalize(), description=description, prix=price, 
                      url_img=images.filename, en_promo=promo, categorie_id=idCat)
    await article.save()

    return templates.TemplateResponse(
        "article_create.html",
        {
            "request": request,
            "id": article.id,
            "libelle": article.libelle,
            "description": article.description,
            "prix": article.prix,
            "categorie": cat.categorie,
            "promotion": article.en_promo
        })

##############################################################################
###### route post createPromo (création promo et mise à jour produit) ########
############### Template: promotion_create.html ##############################

@backOffice.post("/createPromo/", tags=["backOffice"])

# récupération données formulaire création promotion
async def createPromo(request: Request, id_produit: int = Form(...), dateD: str = Form(...),
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

    return templates.TemplateResponse(
        "promotion_create.html",
        {
            "request": request,
            "id_promo": promotion.id,
            "id_article": article.id,
            "dateD": promotion.date_deb,
            "dateF": promotion.date_fin,
            "remise": promotion.remise
        })

@backOffice.get("/prodSelected/{productId}", tags=["backOffice"])

async def prodSelected(productId: int):
    print("id produit:", productId)
    try:
        product = await Produit.get(id=productId)
        return {
            "name": product.libelle,
            "description": product.description,
            "price": product.prix,
            "promotion": product.en_promo
        }
    except DoesNotExist:
        return {
            "name": "Le produit n'existe pas !"
        }
