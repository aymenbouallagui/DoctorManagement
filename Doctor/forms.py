from django import forms
from Doctor.models import visiteur,rendez_vous,payment,medicaments,patient,organism_assur,assuranc , consultation,certif,ordannance
from django.contrib.auth.models import User


class VisitForm(forms.ModelForm):
    class Meta:
        model = visiteur
        fields = ['nom', 'prenom', 'email', 'phone','role']
        widget = {
            'phone': 'required',
        }
        errors = {
            'phone': {
                'required': 'Numero de telephone est obligatoire'
            },

        }


class PatientUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username','password','email']
        widgets = {
            'password': forms.PasswordInput()
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model = patient
        fields = ['phone', 'fixe', 'genre', 'date_naiss', 'code_pays', 'adresse']

class AssuranceForm(forms.ModelForm):
    class Meta:
        model = assuranc
        fields = ['id_assurance', 'id_organism', 'patient']

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = consultation
        fields = ['patient', 'date']

class CertifForm(forms.ModelForm):
    class Meta:
        model = certif
        fields = ['date', 'datedeb', 'datefin', 'description', 'patient']

class OrdenanceForm(forms.ModelForm):
    class Meta:
        model = ordannance
        fields = ['maladies', 'patient','medicaments']

class AssurOrgForm(forms.ModelForm):
    class Meta:
        model = organism_assur
        fields = ['lib_organism']

class PayementForm(forms.ModelForm):
    class Meta:
        model = payment
        fields = ['id_patient', 'cout', 'consult', 'id_methode']

class MedicsForm(forms.ModelForm):
    class Meta:
        model = medicaments
        fields = ['code_barre_med', 'lib_med', 'maladies']

class RdvForm(forms.ModelForm):
    class Meta:
        model = rendez_vous
        fields = ['patient', 'etat_rdv', 'date']