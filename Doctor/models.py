from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class pays (models.Model):
    code_pays = models.IntegerField(primary_key=True, unique=True)
    nom_pays = models.CharField(max_length=30)
    def __str__(self):
        return self.nom_pays
class maladies (models.Model):
    id_maladie = models.AutoField(primary_key=True,unique=True)
    lib_malade = models.CharField(max_length=100)
    def __str__(self):
        return self.lib_malade
class medicaments(models.Model):
    code_med = models.AutoField(primary_key=True, unique=True)
    code_barre_med = models.CharField(max_length=18)
    lib_med = models.CharField(max_length=100)
    maladies = models.ForeignKey(maladies, on_delete=models.CASCADE)
    def __str__(self):
        return self.lib_med

class patient (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    fixe = models.CharField(max_length=50)
    genres = (
        ('m', 'masculain'),
         ('f', 'féminin'),
    )
    genre = models.CharField(choices=genres, max_length=1)
    adresse = models.CharField(max_length=60)
    date_naiss = models.DateField(auto_now=False)
    code_pays = models.ForeignKey(pays, on_delete=models.CASCADE )
    def __str__(self):
        return self.user.username

class organism_assur(models.Model):
    id_organism = models.AutoField(primary_key=True, unique=True)
    lib_organism = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.lib_organism

class assuranc(models.Model):
    id_assurance = models.IntegerField(unique=True,primary_key=True)
    id_organism = models.ForeignKey(organism_assur, on_delete=models.CASCADE)
    patient = models.ForeignKey(patient,on_delete=models.CASCADE)



class historique_maladie (models.Model):
    id_patient = models.ForeignKey(patient, on_delete=models.CASCADE)
    id_maladie = models.ForeignKey(maladies, on_delete=models.CASCADE)

class intervention_ch (models.Model):
    id_patient = models.ForeignKey(patient, on_delete=models.CASCADE)
    id_maladie = models.ForeignKey(maladies, on_delete=models.CASCADE)


class money(models.Model):
    id_money = models.AutoField(primary_key=True, unique=True)
    lib_money = models.CharField(max_length=20)

class payment_methode (models.Model):
    id_methode = models.AutoField(primary_key=True, unique=True)
    lib_methode = models.CharField(max_length=50)
    def __str__(self):
        return self.lib_methode

class rendez_vous (models.Model):
    id_rdv = models.AutoField(primary_key=True, unique=True)
    date = models.DateTimeField(unique=True)
    etat_rdvs = (
        ('1', 'malade'),
        ('2','autre visite'),
    )
    etat_rdv = models.CharField(choices=etat_rdvs, max_length=1)
    patient = models.ForeignKey(patient, on_delete=models.CASCADE)
    canceled = models.BooleanField(default=False)
    def __str__(self):
        return str(self.date)

class consultation (models.Model):
    id_consult = models.AutoField(primary_key=True, unique=True)
    patient = models.ForeignKey(patient, on_delete=models.CASCADE)
    date = models.ForeignKey(rendez_vous, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.date)

class payment (models.Model):
    id_payment = models.AutoField(primary_key=True, unique=True)
    id_patient = models.ForeignKey(patient, on_delete=models.CASCADE)
    cout = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    consult = models.ForeignKey(consultation, on_delete=models.CASCADE)
    id_methode = models.ForeignKey(payment_methode, on_delete=models.CASCADE)




class ordannance (models.Model):
    id_ord = models.AutoField(primary_key=True, unique=True)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True)
    maladies = models.ForeignKey(maladies, on_delete=models.CASCADE)
    patient = models.ForeignKey(patient,on_delete=models.CASCADE)
    medicaments = models.ManyToManyField(medicaments, blank=True)


class certif (models.Model):
    id_certif = models.AutoField(primary_key=True, unique=True)
    date = models.DateField(default=0)
    datedeb = models.DateField(auto_now=False)
    datefin = models.DateField(auto_now=False)
    description = models.CharField(max_length=1450)
    patient = models.ForeignKey(patient,on_delete=models.CASCADE)

class visiteur (models.Model):
    id_v = models.AutoField(primary_key=True,unique=True)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=30)
    ROLES = (
        ('1','Patient'),
        ('2','Autre'),
    )
    role = models.CharField(choices=ROLES, max_length=1)

