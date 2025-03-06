# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from forms import LoginForm, StudentProfileForm, EmployeeProfileForm, AddFriendForm
from Trombinoscoop.models import Personne, Etudiant, Employe, Message
import datetime
from django import forms
from django.http import HttpResponse
from django.core import exceptions


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

        return render_to_response('welcome.html',
                                  {'logged_user': logged_user,
                                   'friendMessages': friendMessages})
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
                return render_to_response('add_friend.html', {'form': form})
        # Le formulaire n'a pas été envoyé
        else:
            form = AddFriendForm()
            return render_to_response('add_friend.html', {'form': form})
    else:
        return HttpResponseRedirect('/login')


def show_profile(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        # Test si le paramètre attendu est bien passé
        if 'userToShow' in request.GET and request.GET['userToShow'] != '':
            results = Personne.objects.filter(id=request.GET['userToShow'])
            if len(results) == 1:
                if Etudiant.objects.filter(id=request.GET['userToShow']):
                    user_to_show = Etudiant.objects.get(id=request.GET['userToShow'])
                else:
                    user_to_show = Employe.objects.get(id=request.GET['userToShow'])
                return render_to_response('show_profile.html',
                                          {'user_to_show': user_to_show})
            else:
                return render_to_response('show_profile.html',
                                          {'user_to_show': logged_user})
        # Le paramètre n'a pas été trouvé
        else:
            return render_to_response('show_profile.html',
                                      {'user_to_show': logged_user})
    else:
        return HttpResponseRedirect('/login')


def login(request):
    # Test si formulaire a été envoyé
    if len(request.GET) > 0:
        form = LoginForm(request.GET)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            logged_user = Personne.objects.get(courriel=user_email)
            request.session['logged_user_id'] = logged_user.id
            return HttpResponseRedirect('/welcome')
        else:
            return render_to_response('login.html', {'form': form})
    # Le formulaire n'a pas été envoyé
    else:
        form = LoginForm()
        return render_to_response('login.html', {'form': form})


def register(request):
    if len(request.GET) > 0:
        form = StudentProfileForm(request.GET)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/login')
        else:
            return render_to_response('login.html', {'form': form})
    else:
        form = StudentProfileForm()
        return render_to_response('user_profile.html', {'form': form})


def register2(request):
    if len(request.GET) > 0 and 'profileType' in request.GET:
        studentForm = StudentProfileForm(prefix="st")
        employeeForm = EmployeeProfileForm(prefix="em")
        if request.GET['profileType'] == 'student':
            studentForm = StudentProfileForm(request.GET, prefix="st")
            if studentForm.is_valid():
                studentForm.save(commit=True)
                return HttpResponseRedirect('/login')
        elif request.GET['profileType'] == 'employee':
            employeeForm = EmployeeProfileForm(request.GET, prefix="em")
            if employeeForm.is_valid():
                employeeForm.save(commit=True)
                return HttpResponseRedirect('/login')
        # Le formulaire envoyé n'est pas valide
        return render_to_response('user_profile2.html',
                                  {'studentForm': studentForm,
                                   'employeeForm': employeeForm})
    else:
        studentForm = StudentProfileForm(prefix="st")
        employeeForm = EmployeeProfileForm(prefix="em")
        return render_to_response('user_profile2.html',
                                  {'studentForm': studentForm,
                                   'employeeForm': employeeForm})


def modify_profile(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if len(request.GET) > 0:
            if type(logged_user) == Etudiant:
                form = StudentProfileForm(request.GET, instance=logged_user)
            else:
                form = EmployeeProfileForm(request.GET, instance=logged_user)
            if form.is_valid():
                form.save(commit=True)
                return HttpResponseRedirect('/welcome')
            else:
                return render_to_response('modify_profile.html', {'form': form})
        else:
            if type(logged_user) == Etudiant:
                form = StudentProfileForm(instance=logged_user)
            else:
                form = EmployeeProfileForm(instance=logged_user)
            return render_to_response('modify_profile.html', {'form': form})
    else:
        return HttpResponseRedirect('/login')


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