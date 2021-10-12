import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required ,user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from Doctor import forms

from django.contrib.auth.models import Group, User
from django.contrib import messages
from Doctor.models import visiteur,medicaments,organism_assur,payment,historique_maladie,organism_assur
from Doctor.models import ordannance,certif,consultation,patient,rendez_vous,assuranc,payment_methode
from django.utils import timezone
from django import template
# /// Welcome Page ///



def welcome(request):
    submitbutton = request.POST.get('SUBMIT')
    form = forms.VisitForm()
    if submitbutton:
        if request.method == 'POST':
            form =forms.VisitForm(request.POST)
            if form.is_valid():
                form.save()
    return render(request, 'Doctor/index.html', {'form': form})



#  /// Sign in ///

def signinuser(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    context = {'userForm':userForm,'patientForm':patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.save()
            patient_group = Group.objects.get_or_create(name='PATIENT')
            patient_group[0].user_set.add(user)
            return redirect('/login')
    return render(request, 'Doctor/patientcreateaccount.html', context)


#  /// Login ///
def loginview (request):
    context = {}
    submitbutton1 = request.POST.get('LOGIN')
    if submitbutton1:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user1 = authenticate(request, username=username, password=password)
            if user1 is not None:
                login(request, user1)
                return redirect('/afterlog/{pk}'.format(pk=username))
            else:
                messages.info(request,'Username OR password is incorrect')
            context = {}
    return render(request, 'Doctor/login.html', context)

# User OR Admin testing
@login_required(login_url='login')
def afterlogin(request,pk):
    if is_patient(request.user):
        return redirect('/dashboard/{pk}'.format(pk=pk))
    else:
        return redirect('/doctordash1')

#PATIENT TESTING ABOUT
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

#ADMIN TESTING ABOUT
def is_Admin(user):
    return not is_patient(user)


# ///   interface Ordennance et certifs  ///
@login_required(login_url='login')
@user_passes_test(is_patient)
def PatientDash1 (request, pk):
    obj = get_object_or_404(User, username=pk)
    pat = obj.patient
    orden = ordannance.objects.filter(patient=pat)
    certi = certif.objects.filter(patient=pat)
    context = {'pat': pat, 'orden': orden, 'certi': certi, 'obj': obj}
    return render(request, 'Doctor/dashboarduser.html', context)


# ///   interface rendez vous ///
@login_required(login_url='login')
@user_passes_test(is_patient)
def PatientDash2 (request, pk):
    v = visiteur()
    submitbutton2 = request.POST.get('RDV')
    rdv_future = []
    rdv_past = []
    obj = get_object_or_404(User, username=pk)
    pat = obj.patient
    now = timezone.now()
    if submitbutton2:
        v.nom = obj.first_name
        v.prenom = obj.last_name
        v.email = obj.email
        v.phone = pat.phone
        v.role = 'Patient'
        v.save()
    for i in rendez_vous.objects.filter(patient=pat):
        if i.date >= now:
            rdv_future.append(i)
        else:
            rdv_past.append(i)
    context = {'rdv_future': rdv_future, 'rdv_past': rdv_past}
    return render(request, 'Doctor/dashboarduserrendez.html', context)


# ///   interface Assurance USER ///
@login_required(login_url='login')
@user_passes_test(is_patient)
def PatientDash3 (request, pk):
    submitbutton3 = request.POST.get('ASSUR')
    form = forms.AssuranceForm()
    obj = get_object_or_404(User, username=pk)
    if submitbutton3:
        a = assuranc()
        if request.method == 'POST':
            form = forms.AssuranceForm(request.POST)
            a.id_assurance = form['id_assurance'].value()
            a.id_organism = organism_assur.objects.get(id_organism=int(form['id_organism'].value()))
            a.patient = obj.patient
            a.save()
    pat = obj.patient
    assur = assuranc.objects.filter(patient=pat)
    context = {'assur': assur, 'obj': obj, 'form': form}
    return render(request, 'Doctor/dashboarduserassurances.html', context)

# /// Logout ///
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('/')



#////////////      ADMIN CODE ZONE /////////////////////////////


@login_required(login_url='login')
@user_passes_test(is_Admin)
def DoctorDash1(request):
    monthconsult = 0
    dayconsult = 0
    now = timezone.now()
    lista1 = []
    lista2 = []
    lista3 = []
    lista4 = []
    count = 0
    count1 = 0
    count2 = 0
    aux = 0
    aux2 = patient()
    age_sum = 0
    for i in patient.objects.all():
        count += 1
        age_sum += now.year - i.date_naiss.year
    if count != 0:
        moy_age = age_sum / count
    for i in consultation.objects.all():
        rdv = i.date
        if rdv.date.year == now.year and rdv.date.month == now.month:
            monthconsult += 1
        if rdv.date.year == now.year and rdv.date.month == now.month and rdv.date.day == now.day :
            dayconsult += 1
    for i in patient.objects.all():
        for j in rendez_vous.objects.all():
            if j.patient == i and j.canceled:
                count1 += 1
        if count1 > 0:
            lista1.append(i)
            lista2.append(count1)
            count1 = 0
    for i in patient.objects.all():
        for j in consultation.objects.all():
            if j.patient == i:
                count2 += 1
        if count2 > 0:
            lista3.append(i)
            lista4.append(count2)
            count2 = 0
    for i in lista2:
        for j in range(i+1, len(lista2)):
            if lista2[i] < lista2[j]:
                aux = lista2[i]
                lista2[i] = lista2[j]
                lista2[j] = aux
                aux2 = lista1[i]
                lista1[i] = lista1[j]
                lista1[j] = aux2
    for i in lista4:
        for j in range(i + 1, len(lista4)):
            if lista4[i] < lista4[j]:
                aux = lista4[i]
                lista4[i] = lista4[j]
                lista4[j] = aux
                aux2 = lista3[i]
                lista3[i] = lista3[j]
                lista3[j] = aux2
    count018mas = 0
    count018fem = 0
    count1935mas = 0
    count1935fem = 0
    count3660mas = 0
    count3660fem = 0
    count61mas = 0
    count61fem = 0
    for i in patient.objects.all():
        if (now.year - i.date_naiss.year) in range(-1, 18):
            if i.genre == 'm':
                count018mas += 1
            else:
                count018fem += 1
        if (now.year - i.date_naiss.year) in range(19, 35):
            if i.genre == 'm':
                count1935mas += 1
            else:
                count1935fem += 1
        if (now.year - i.date_naiss.year) in range(36, 60):
            if i.genre == 'm':
                count3660mas += 1
            else:
                count3660fem += 1
        else:
            if i.genre == 'm':
                count61mas += 1
            else:
                count61fem += 1
    context = {'age_moy': moy_age,
               'nbrpatient': count,
               'monthconsult': monthconsult,
               'dayconsult': dayconsult,
               'list_pat_annul': lista1,
               'annul_times': lista2,
               'patient_suivi': lista3,
               'suivi_times': lista4,
               'count018mas': count018mas,
               'count018fem': count018fem,
               'count1935mas': count1935mas,
               'count1935fem': count1935fem,
               'count3660mas': count3660mas,
               'count3660fem': count3660fem,
               'count61mas': count61mas,
               'count61fem': count61fem,
               }
    return render(request, 'Doctor/dashboarddoc.html', context)

@login_required(login_url='login')
@user_passes_test(is_Admin)
def DoctorDash2(request):
    form = forms.RdvForm()
    rdv = rendez_vous.objects.all()
    vis = visiteur.objects.all()
    context = {
        'form': form,
        'vis': vis,
        'rdv': rdv
        }
    if request.method == 'POST':
        form = forms.RdvForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'Doctor/dashboarddoccalendar.html', context)

@login_required(login_url='login')
@user_passes_test(is_Admin)
def DoctorDash3(request):
    now = timezone.now()
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    user = User.objects.all()
    assu = assuranc.objects.all()
    hist_mala = historique_maladie.objects.all()

    context = {'userForm': userForm,
               'patientForm': patientForm,
               'user': user,
               'yearnow': now.year,
               'assu': assu,
               'hist_mala': hist_mala,
               }
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.save()
            patient_group = Group.objects.get_or_create(name='PATIENT')
            patient_group[0].user_set.add(user)
            redirect('/doctordash3')
    return render(request,'Doctor/dashboarddocpatients.html',context)

@login_required(login_url='login')
@user_passes_test(is_Admin)
def DoctorDash4(request):
    form = forms.ConsultationForm()
    consu = []
    count = 0
    for i in consultation.objects.all():

        for j in payment.objects.all():
            con = j.consult
            if con == i:
                count += 1
        if count == 0:
            consu.append(i)
        count = 0
    context = {
        'form': form,
        'consu': consu
    }
    if request.method == 'POST':

        form = forms.ConsultationForm(request.POST)
        if form.is_valid():

            form.save()
    return render(request,'Doctor/dashboarddocconsultation.html',context)

@login_required(login_url='login')
@user_passes_test(is_Admin)
def DoctorDash5(request):
    form = forms.CertifForm()
    cer = certif.objects.all()
    context = {
        'form': form,
        'cer': cer
    }
    if request.method == 'POST':
        print('aaaaaaaaaaaaaa')
        form = forms.CertifForm(request.POST)
        print('ccccccccccccccc')
        if form.is_valid():
            print('bbbbbbbbbb')
            form.save()
            print('ddddddddddddddddddd')
    return render(request, 'Doctor/dashboarddoccertif.html', context)


@login_required(login_url='login')
@user_passes_test(is_Admin)
def DoctorDash6(request):
    form = forms.OrdenanceForm()
    ord = ordannance.objects.all()
    context = {
        'form': form,
        'ord': ord
    }
    if request.method == 'POST':
        form = forms.OrdenanceForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'Doctor/dashboarddocordenance.html', context)

@login_required(login_url='login')
@user_passes_test(is_Admin)
def DoctorDash7(request):
    form = forms.AssurOrgForm()
    assuorg = organism_assur.objects.all()
    context = {'form': form,
               'assuorg': assuorg
               }
    if request.method == 'POST':
        form = forms.AssurOrgForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request,'Doctor/dashboarddocassurance.html',context)

@login_required(login_url='login')
@user_passes_test(is_Admin)
def DoctorDash8(request):
    pay = payment.objects.all()
    context = {
        'pay': pay
    }
    return render(request, 'Doctor/dashboarddocpaiement.html', context)


@login_required(login_url='login')
@user_passes_test(is_Admin)
def DoctorDash9(request):
    form = forms.MedicsForm()
    meds = medicaments.objects.all()
    context = {
        'form': form,
        'meds': meds
    }
    if request.method == 'POST':
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        form = forms.MedicsForm(request.POST)
        print('vvvvvvvvvvvvvvv')
        if form.is_valid():
            print('yyyyyyyyyyyyyyyyyy')
            form.save()
    return render(request, 'Doctor/dashboarddocmeds.html', context)

@login_required(login_url='login')
@user_passes_test(is_Admin)
def edit_patient(request,pk):
    user = get_object_or_404(User, username=pk)
    patient = user.patient
    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    context = {'userForm': userForm,
               'patientForm': patientForm,
               'user': user,
               }
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST,instance=user)
        patientForm = forms.PatientForm(request.POST,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patientForm.save()
        return HttpResponseRedirect('/doctordash3')
    return render(request, 'Doctor/dashboarddoceditpatient.html', context)


@login_required(login_url='login')
@user_passes_test(is_Admin)
def delete_patient(request, pk):
    user = User.objects.get(username=pk)
    patient = user.patient
    user.delete()
    patient.delete()
    return redirect('/doctordash3')

@login_required(login_url='login')
@user_passes_test(is_Admin)
def delete_certif(request, pk):
    cer = certif.objects.get(id_certif=pk)
    cer.delete()
    return redirect('/doctordash6')

@login_required(login_url='login')
@user_passes_test(is_Admin)
def payer(request, pk):
    consult = consultation.objects.get(id_consult=pk)
    pa = consult.patient
    form = forms.PayementForm()
    paybutton = request.POST.get('pay')
    context = {
        'form': form
    }
    if paybutton:
        p = payment()
        if request.method == 'POST':
            form = forms.PayementForm(request.POST)
            p.id_patient = pa
            p.consult = consult
            p.cout = form['cout'].value()
            p.id_methode = payment_methode.objects.get(id_methode=int(form['id_methode'].value()))
            p.save()
            return redirect('/doctordash4')
    return render(request, 'Doctor/doctordashpayer.html', context)

@login_required(login_url='login')
@user_passes_test(is_Admin)
def delete_medic(request, pk):
    med = medicaments.objects.get(code_med=pk)
    med.delete()
    return redirect('/doctordash9')
