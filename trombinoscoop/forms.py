# -*- coding: utf-8 -*-

from django import forms
from Trombinoscoop.models import Personne, Etudiant, Employe


class LoginForm(forms.Form):
    email = forms.EmailField(label='Courriel :')
    password = forms.CharField(label='Mot de passe :',
                               widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        # Vérifie que les deux champs sont valides
        if email and password:
            result = Personne.objects.filter(mot_de_passe=password,
                                             courriel=email)
            if len(result) != 1:
                raise forms.ValidationError("Adresse de courriel ou mot de passe erroné.")

        return cleaned_data


class AddFriendForm(forms.Form):
    email = forms.EmailField(label='Courriel :')

    def clean(self):
        cleaned_data = super(AddFriendForm, self).clean()
        email = cleaned_data.get("email")

        # Vérifie que le champ est valide
        if email:
            result = Personne.objects.filter(courriel=email)
            if len(result) != 1:
                raise forms.ValidationError("Adresse de courriel erronée.")

        return cleaned_data


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        exclude = ('amis',)


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = Employe
