from tortoise import fields
from tortoise.models import Model

############## config des modèles ORM ######################

class Promotion(Model):
    id = fields.IntField(pk=True, auto_icrement=True)
    remise = fields.DecimalField(max_digits= 4,decimal_places= 2)      
    date_deb = fields.DateField()
    date_fin = fields.DateField()

    def __str__(self):
        return self.remise + "\%% du:" + self.date_deb + ' au:' + self.date_fin
    
class Produit(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    libelle = fields.CharField(max_length= 50)
    description = fields.TextField()
    prix = fields.DecimalField(max_digits= 6, decimal_places= 2)
    url_img = fields.CharField(max_length= 50)
    en_promo = fields.BooleanField()
    promotion = fields.ForeignKeyField('models.Promotion', related_name='produits')
    categorie = fields.CharField(max_length=40)

    def __str__(self):
        return str(self.en_promo)
    
class Admin(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    mail = fields.CharField(max_length=100 , unique=True)
    password = fields.CharField(max_length=100, unique=True)