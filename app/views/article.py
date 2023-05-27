from fastapi import APIRouter, Request, HTTPException, Form, UploadFile, File, Depends
from fastapi.responses import RedirectResponse

from app.models.article import Produit, Admin, Promotion, Categorie
from app.core.myconfig import templates, S3

# importe fonction custom de vérification mail et password en bdd
from app.verify import verifyPasswordMail
# importe fonction custom de prévention SQL injection
from app.sqli import sql_i_injection

#librairie pour générer token
import jwt  
#librairie pour variables locales
from decouple import config

# librarie gestion erreur ORM Tortoise
from tortoise.exceptions import DoesNotExist, OperationalError
# librairie boto gestion erreurs
from botocore.exceptions import BotoCoreError, NoCredentialsError
# librairie pour création PDF
from borb.pdf import Document, Page, SingleColumnLayout, Paragraph, \
     PDF, PageLayout, Image, Alignment

from decimal import Decimal
# librairie pour dater pdf
from datetime import date
from io import BytesIO

#####################################################

homePage = APIRouter()       # route public
articlesViews = APIRouter()  # route public
adminConnect = APIRouter()   # route public
backOffice = APIRouter()     # route privé
exportPDF = APIRouter()  

###### fonctions générateur token ########

def generateToken(payload: dict) ->str:
    
    return jwt.encode(payload, key_JWT, algorithm="HS256")

######### fonction récupération et vérification token dans session et gestion erreur ####
async def get_verify_token(request: Request):

    #récupération token
    token = request.session.get("token")
    # si pas de token
    if not token:
        raise HTTPException(status_code=401, detail="Accès non autorisé - pas de token !")
    # sinon essai decodage
    else:
        try:
            jwt.decode(token, key_JWT, algorithms=["HS256"])
            return token
        except (jwt.DecodeError, jwt.InvalidKeyError, jwt.InvalidTokenError):
            raise HTTPException(status_code=401, detail="Accès non autorisé - token invalide !")

#################### type hints ####################

valid: bool  #related function login (route /DataForm)
nosqli: bool  
payload: dict
idCat: int  #related function creteProd (route /createProd)
token: str  #related function get_token_verify
key_JWT: str = config("JWT_SECRETKEY")  # (local)

######################################################
############ route GET / Page d'accueil ##############
######## template:  index.html   #####################

@homePage.get("/", tags=["home"])
async def root(request: Request): 
    
    # efface le token
    request.session["token"] = ""

    return templates.TemplateResponse("index.html", { "request": request })

######################################################
############### route GET /articles ##################
########## Template products_list.html ###############

@articlesViews.get("/articles/", tags=["articles"])
# par défaut filter = "libellé" --> tous les articles
async def articles_list(request: Request, filter: str = "libelle"):

    # récupération de toutes les catégories en BDD pour liste déroulante
    categories = await Categorie.all()
    # capture du filtre pour message mémoire CATEGORIE
    libelleCategorie = filter

    # afficher les produits selon le filtre sélectionné avec gestion erreur
    match filter:
        case "libelle":
            try:
                # requetes avec jointure sur tables produit , promotion et categorie
                produits = await Produit.all().prefetch_related('promotion', 'categorie')
            except OperationalError as e:
                raise HTTPException(status_code=500, 
                                    detail="Erreur pour récupérer les articles du catalogue. " + str(e))
        case _:
            try:
                produits = await Produit.filter(categorie=filter).prefetch_related('promotion', 'categorie')
                # récupération du nouveau libellé catégorie pour message mémoire CATEGORIE
                libelleCategorie = await Categorie.filter(id=filter)
            except OperationalError as e:
                raise HTTPException(status_code=500, 
                                    detail=f"Erreur pour récupérer les articles filtrés sur {filter} du catalogue. " + str(e))
        
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
async def login(request: Request, email: str = Form(...), password: str = Form(...)):

    # verification SQLi sur email et password --> fonction (sqli.py)
    nosqli = sql_i_injection(email)
    if nosqli == False:
        nosqli = sql_i_injection(password)

        if nosqli == False:
            # si pas d'injections repérées requete BDD pour récupérér les données admin
            try:
                users = await Admin.all()  ###1 haché/salé email puis users = await Admin.get(mail=email_hashed)
            except OperationalError as e:
                raise HTTPException(status_code=500, 
                                    detail="Erreur de lecture pour l'administrateur. " + str(e))    
        else:
            # sinon redirection page d'accueil
            return RedirectResponse(url="/", status_code=205)
    else:
        return RedirectResponse(url="/", status_code=205)

    # recherche parmi les données admin (1 seul admin) si plusieurs admin modif ###1
    for user in users:   
        # fonction (verify.py) verification email et password du formulaire avec BDD
        valid = verifyPasswordMail(email, password, user.mail, user.password)

        ##### réponse si identifiants valides
        if valid == True:
            # génération token d'authentification avec email/password du formulaire
            # sauvegarde token dans la session et redirection /BOffice    
            payload= {f"{email}":f"{password}"}
            request.session["token"] = generateToken(payload)
            return RedirectResponse(url='/BOffice/', status_code=303)
        # sinon retour accueil
        else:
            return RedirectResponse(url="/", status_code=303)

########################################################
################# routes BackOffice ####################
####### injection dépendance (get_verify_token)  #######
############ Template: Boffice.html  ###################

########  route GET page d'accueil du Back Office ######        
@backOffice.get("/BOffice/", dependencies=[Depends(get_verify_token)], tags=["backOffice"])
async def adminBackOffice(request: Request):

    return templates.TemplateResponse( "Boffice.html", { "request": request })

####### route post createProd (création produit) ########
######## Template: article_create.html ##################

@backOffice.post("/createProd/", dependencies=[Depends(get_verify_token)], tags=["backOffice"])
# récupération des données formulaire création produit
async def createProd(request: Request, label: str = Form(...), description: str = Form(...),
                     price: float = Form(...), promo: str = Form(...), 
                     images: UploadFile = File(...) , categorie: str = Form(...)):
    
    # Valrus opérateur promo reçoit True ou False selon le résultat du test promo == "on"
    promo = (val := promo == "on")

    try:
        # récupération de l'id de la catégorie donnée
        cat = await Categorie.get(categorie=categorie)
        idCat = cat.id 
    # si nouvelle catégorie - création catégorie et récupération de son id
    except DoesNotExist:
        cat = Categorie(categorie=categorie)
        await cat.save()
        idCat = cat.id

    # téléversement du fichier image à partir du répertoire local au bucket s3
    try:
        S3.s3_client.upload_fileobj(images.file, S3.bucket_name, images.filename)
    except (BotoCoreError, NoCredentialsError) as e:
        return {"erreur": "Impossible de téléverser l'image au Bucket S3: {}".format(str(e))}

    try:
        #composition de l'article et enregistrement dans la table avec l'id catégorie
        article = Produit(libelle=label.capitalize(), description=description, prix=price, 
                          url_img=images.filename, en_promo=promo, categorie_id=idCat)
        await article.save()
    except OperationalError as e:
        raise HTTPException(status_code=500, 
                            detail="Erreur d'enregistrement du produit. " + str(e))

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

######################################################################
### route post createPromo (création promo et mise à jour produit) ###
############# injection dépendance (get_verify_token)  ###############
################# Template: promotion_create.html ####################

@backOffice.post("/createPromo/", dependencies=[Depends(get_verify_token)], tags=["backOffice"])
# récupération données formulaire création promotion
async def createPromo(request: Request, id_produit: int = Form(...), dateD: str = Form(...),
                      dateF: str = Form(...), remise: int = Form(...)):

    # composition de la promotion et enregistrement
    try:
        promotion = Promotion(remise=remise, date_deb=dateD, date_fin=dateF)
        await promotion.save()
    except OperationalError as e:
        raise HTTPException(status_code=500, 
                            detail="Erreur d'enregistrement de la promotion. " + str(e))

    # mise a jour du produit sélectionné avec la promotion
    try:
        article = await Produit.get(id=id_produit)
        article.promotion_id = promotion.id
        article.en_promo = True
        await article.save()
    except OperationalError as e:
        raise HTTPException(status_code=500, 
                            detail="Erreur de mise à jour du produit. " + str(e))

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

##################################################################
######## route GET prodSelected pour caractéristique produit #####
############# injection dépendance (get_verify_token)  ###########

@backOffice.get("/prodSelected/{productId}", dependencies=[Depends(get_verify_token)], tags=["backOffice"])
async def prodSelected(productId: int):

    # récupère catactéristiques du produit selon id et renvoi au template
    try:
        product = await Produit.get(id=productId)
        
        if product.en_promo == True:
            promo = "Oui" 
        else:
            promo = "Non"
        
        return {
            "name": product.libelle,
            "description": product.description,
            "price": product.prix,
            "promotion": promo
        }
    except DoesNotExist:
        return {"name": "Le produit n'existe pas !"}
    
##################################################################
####### route GET fonction Exportation en PDF ####################
############# injection dépendance (get_verify_token)  ###########

@exportPDF.get("/export-pdf", dependencies=[Depends(get_verify_token)], tags=["backOffice"])
async def export_pdf():
    #recupère les produits
    produits = await Produit.all().prefetch_related('promotion')
    #calcul le nombre de page du pdf
    nbrprod = round(len(produits)/3)
    # date du jour au format FR
    today = date.today()
    todayFormat = today.strftime("%d-%m-%Y")
    #crée un PDF
    pdf: Document = Document()
    layout, a = generate_new_page(pdf)
    #crée une entete
    layout.add(Paragraph(f"CATALOGUE MERCADONA du {todayFormat} - PAGE: {a} / {nbrprod}"))
    layout.add(Paragraph(""))
    # itère sur les produits
    for produit in produits:
        #ajoute une page au pdf tous les 3 produits avec nouveau layout et entete
        if a%4 == 0:
            layout, a = generate_new_page(pdf)

        #compose les paragraphes du pdf
        if (produit.en_promo == True):
            promo = produit.promotion
            produitSolde = str(round(produit.prix - (produit.prix*promo.remise)/100, 2)) + " euros"
            produitPromotion = f"{promo.date_deb} / {promo.date_fin} / taux: {promo.remise} %"
        else:
            produitPromotion = "---" 
            produitSolde = "---"

        layout.add(Paragraph(f"ID Produit: {produit.id}", font_size=Decimal(9) ))
        layout.add(Paragraph(f"Libellé: {produit.libelle} Prix initial: {produit.prix} euros", font_size=Decimal(9)))
        layout.add(Paragraph(f"Description: {produit.description}", font_size=Decimal(9) ))
        layout.add(Paragraph(f"Promotion: {produitPromotion}", font_size=Decimal(9) ))
        layout.add(Paragraph(f"Prix soldé: {produitSolde}", font_size=Decimal(9) ))
        layout.add(Image(f"https://{S3.bucket_name}.s3.eu-west-3.amazonaws.com/{produit.url_img}",
                            width=Decimal(60),
                            height=Decimal(60)
              ))  
        layout.add(Paragraph("_"*65))
        a+=1

    # téléversement du pdf au bucket s3 PDF
    try:
        # appel fonction de convertion
        doc_bytes: bytes = PDF_to_Bytes(pdf)
        #composition du filename PDF
        filenamePDF = f"mercadonaPDF_{todayFormat}.pdf"
        S3.s3_client.upload_fileobj(BytesIO(doc_bytes), S3.bucket_pdf, filenamePDF)
    except (BotoCoreError, NoCredentialsError) as e:
        return {"erreur": "Impossible de téléverser le PDF au Bucket S3: {}".format(str(e))} 
    #composition du path S3 du PDF
    path_PDF = f"https://mercastatic-pdf.s3.amazonaws.com/{filenamePDF}"
    return {"PDF": f"Le PDF {filenamePDF} est crée avec succès -->",
            "PATH": f"{path_PDF}"}
    
# fonction de convertion du document en bytes
def PDF_to_Bytes(pdf: Document) ->bytes :
    # Création d'un objet BytesIO en mémoire pour stocker le contenu PDF
    pdf_buffer = BytesIO()
    # Écriture du contenu PDF dans l'objet BytesIO
    PDF.dumps(pdf_buffer, pdf)
    # Réinitialisation de la position du curseur dans le buffer
    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()

def generate_new_page(pdf):
    #compteur de produits réinitialisé a 1 tous les 3 produits
    a = 1
    page: Page = Page()
    pdf.add_page(page)
    layout: PageLayout = SingleColumnLayout(page,
                                            horizontal_margin= Decimal(15),
                                            vertical_margin=Decimal(30))
    return layout, a
