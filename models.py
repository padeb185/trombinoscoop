# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
# -*- coding: utf-8 -*-

from django.db import models

class Faculte(models.Model):
  nom = models.CharField(max_length=30)
  couleur = models.CharField(max_length=6, blank=True)
  def __unicode__(self):
      return self.nom

# Personne simplifiée
#class Personne(models.Model):
#  matricule = models.CharField(max_length=10)
#  nom = models.CharField(max_length=30)
#  prenom = models.CharField(max_length=30)
#  date_de_naissance = models.DateField()
#  courriel = models.EmailField()
#  tel_fixe = models.CharField(max_length=20)
#  tel_mobile = models.CharField(max_length=20)
#  mot_de_passe = models.CharField(max_length=32)


class Personne(models.Model):
  nom = models.CharField(max_length=30)
  prenom = models.CharField(max_length=30)
  date_de_naissance = models.DateField()
  matricule = models.CharField(max_length=10)
  courriel = models.EmailField()
  tel_fixe = models.CharField(max_length=20)
  tel_mobile = models.CharField(max_length=20)
  amis = models.ManyToManyField("self", blank=True)
  mot_de_passe = models.CharField(max_length=32)
  faculte = models.ForeignKey(Faculte)
  def __unicode__(self):
      return self.prenom + " " + self.nom
#
class Campus(models.Model):
  nom = models.CharField(max_length=30)
  adresse_postale = models.CharField(max_length=60)
  def __unicode__(self):
      return self.nom

class Fonction(models.Model):
  intitule = models.CharField(max_length=30)
  def __unicode__(self):
      return self.intitule

class Employe(Personne):
  bureau = models.CharField(max_length=30)
  campus = models.ForeignKey(Campus)
  fonction = models.ForeignKey(Fonction)

class Cursus(models.Model):
  intitule = models.CharField(max_length=30)
  def __unicode__(self):
      return self.intitule

class Etudiant(Personne):
  cursus = models.ForeignKey(Cursus)
  annee = models.IntegerField()

class Message(models.Model):
  auteur = models.ForeignKey(Personne)
  contenu = models.TextField()
  date_de_publication = models.DateField()
  def __unicode__(self):
      if len(self.contenu) > 20:
          return self.contenu[0:19] + "..."
      else:
          return self.contenu