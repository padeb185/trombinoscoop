# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect  # Remplace render_to_response par render
from django.http import HttpResponse, HttpResponseRedirect
from django.core import exceptions
from django import forms
import datetime

# Import des formulaires de l'application locale
from trombinoscoop.forms import LoginForm, StudentProfileForm, EmployeeProfileForm, AddFriendForm

# Import des modèles de l'application locale
from trombinoscoop.models import Personne, Etudiant, Employe, Message


def get_logged_user_from_request(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session['logged_user_id']
        # On cherche un étudiant
        if len(Etudiant.objects.filter(id=logged_user_id)) == 1:
            return Etudiant.objects.get(id=logged_user_id)
        # On cherche un Employé
        elif len(Employe.objects.filter(id=logged_user_id)) == 1:
            return Employe.objects.get(id=logged_user_id)
        # Si on n'a rien trouvé
        else:
            return None
    else:
        return None


def welcome(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if 'newMessage' in request.GET and request.GET['newMessage'] != '':
            newMessage = Message(auteur=logged_user,
                                 contenu=request.GET['newMessage'],
                                 date_de_publication=datetime.date.today())
            newMessage.save()

        friendMessages = Message.objects.filter(auteur__amis=logged_user).order_by('-date_de_publication')

        return render(request, 'welcome.html', {
            'logged_user': logged_user,
            'friendMessages': friendMessages
        })
    else:
        return HttpResponseRedirect('/login')


def add_friend(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        # Test si formulaire a été envoyé
        if len(request.GET) > 0:
            form = AddFriendForm(request.GET)
            if form.is_valid():
                new_friend_email = form.cleaned_data['email']
                newFriend = Personne.objects.get(courriel=new_friend_email)
                logged_user.amis.add(newFriend)
                logged_user.save()
                return HttpResponseRedirect('/welcome')
            else:
                return render(request, 'add_friend.html', {'form': form})

            # Le formulaire n'a pas été envoyé
        else:
            form = AddFriendForm()
            return render(request, 'add_friend.html', {'form': form})
    return HttpResponseRedirect('/login')


def show_profile(request):
    logged_user = get_logged_user_from_request(request)

    if not logged_user:
        return redirect('login')  # Assurez-vous que l'URL "login" est définie dans urls.py

    user_to_show = logged_user  # Valeur par défaut

    # Vérifie si le paramètre `userToShow` est présent et non vide
    user_id = request.GET.get('userToShow', '').strip()
    if user_id:
        person = Personne.objects.filter(id=user_id).first()
        if person:
            # Vérifie s'il s'agit d'un étudiant ou d'un employé
            user_to_show = Etudiant.objects.filter(id=user_id).first() or Employe.objects.filter(id=user_id).first()

    return render(request, 'show_profile.html', {'user_to_show': user_to_show})
def login(request):
    if request.method == "POST":  # Vérifie si le formulaire a été soumis en POST
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']

            try:
                logged_user = Personne.objects.get(courriel=user_email)
                request.session['logged_user_id'] = logged_user.id
                return redirect('welcome')  # Utilisation du nom de l'URL pour plus de flexibilité
            except Personne.DoesNotExist:
                form.add_error('email', "Utilisateur non trouvé.")  # Ajoute une erreur au formulaire

    else:
        form = LoginForm()  # Formulaire vide si aucune donnée envoyée

    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == "POST":  # Vérifie si le formulaire a été soumis en POST
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            form.save(commit=True)  # Enregistre l'utilisateur dans la base de données
            return redirect('login')  # Redirige vers la page de connexion
    else:
        form = StudentProfileForm()  # Formulaire vide si aucune donnée envoyée

    return render(request, 'user_profile.html', {'form': form})


def register2(request):
    studentForm = StudentProfileForm(prefix="st")
    employeeForm = EmployeeProfileForm(prefix="em")

    if request.method == "POST" and 'profileType' in request.POST:
        profile_type = request.POST['profileType']

        if profile_type == 'student':
            studentForm = StudentProfileForm(request.POST, prefix="st")
            if studentForm.is_valid():
                studentForm.save(commit=True)
                return redirect('login')  # Redirige vers la page de connexion

        elif profile_type == 'employee':
            employeeForm = EmployeeProfileForm(request.POST, prefix="em")
            if employeeForm.is_valid():
                employeeForm.save(commit=True)
                return redirect('login')  # Redirige vers la page de connexion

        # Si les formulaires ne sont pas valides, on retourne à la page avec les erreurs
        return render(request, 'user_profile2.html', {
            'studentForm': studentForm,
            'employeeForm': employeeForm
        })

    return render(request, 'user_profile2.html', {
        'studentForm': studentForm,
        'employeeForm': employeeForm
    })


def modify_profile(request):
    logged_user = get_logged_user_from_request(request)

    if logged_user:
        # Vérification si le formulaire a été soumis
        if request.method == "POST":
            if isinstance(logged_user, Etudiant):
                form = StudentProfileForm(request.POST, instance=logged_user)
            else:
                form = EmployeeProfileForm(request.POST, instance=logged_user)

            if form.is_valid():
                form.save(commit=True)
                return redirect('welcome')  # Redirection vers la page de bienvenue
            else:
                return render(request, 'modify_profile.html', {'form': form})

        # Si le formulaire n'a pas été soumis, afficher un formulaire vide ou avec les données existantes
        else:
            if isinstance(logged_user, Etudiant):
                form = StudentProfileForm(instance=logged_user)
            else:
                form = EmployeeProfileForm(instance=logged_user)

            return render(request, 'modify_profile.html', {'form': form})

    else:
        return redirect('login')

def ajax_check_email_field(request):
    HTML_to_return = ''
    if 'value' in request.GET:
        field = forms.EmailField()
        try:
            field.clean(request.GET['value'])
        except exceptions.ValidationError as ve:
            HTML_to_return = '<ul class="errorlist">'
            for message in ve.messages:
                HTML_to_return += '<li>' + message + '</li>'
            HTML_to_return += '</ul>'

    return HttpResponse(HTML_to_return)


def ajax_add_friend(request):
    HTML_to_return = ''
    logged_user = get_logged_user_from_request(request)
    if not logged_user is None:
        if 'email' in request.GET:
            new_friend_email = request.GET['email']
            if len(Personne.objects.filter(courriel=new_friend_email)) == 1:
                new_friend = Personne.objects.get(courriel=new_friend_email)
                logged_user.amis.add(new_friend)
                logged_user.save()

                HTML_to_return = '<li><a href="show_profile?userToShow='
                HTML_to_return += str(new_friend.id)
                HTML_to_return += '">'
                HTML_to_return += new_friend.prenom + ' ' + new_friend.nom
                HTML_to_return += '</a></li>'

    return HttpResponse(HTML_to_return)