from django.db import models
from django.contrib.auth.models import User


class Taktika(models.Model):
    createdAt = models.dateTimeField()
    user = models.ForeignKey(User)
    initConfig = models.charField(max_length=100)
    movesWhite = models.charField(max_length=3000)
    movesBlack = models.charField(max_length=3000)
    tezina = models.DecimalField()
    brojGlasova = models.IntegerField()

class RjesenjeTaktike(models.Model):
    user = models.ForeignKey(User)
    vrijeme = models.DecimalField()

class DojavaPogreske(models.Model):
    taktika = models.ForeignKey(Taktika)
    userDojave = models.ForeignKey(User)
    userRevizija = models.ForeignKey(User)
    prihvacena = models.BooleanField()
    predlozeniTijek = models.charField(max_length=6000)

class RangLista(models.Model):
    user = models.ForeignKey(User)
    bodovi = models.IntegerField()

class Novost(models.Model):
    user = models.ForeignKey(User)
    vrijemeObjave = models.dateTimeField()
    naslov = models.charField(max_length=100)
    tekst = models.charField(max_length=3000)

class Trening(models.Model):
    organizator = models.ForeignKey(User)
    vrijemePocetka = models.dateTimeField()
    vrijemeZavrsetka = models.dateTimeField()
    opisTreninga = models.charField(max_length=100)

class PrijavaTrening(models.Model):
    trening = models.ForeignKey(Trening)
    user = models.ForeignKey(User)

class Turnir(models.Model):
    formatTurnira = models.charField(max_length=100)
    vrijemePocetka = models.dateTimeField()
    vrijemeZavrsetka = models.dateTimeField()
    brojSudionika = models.IntegerField()

class PrijavaTurnir(models.Model):
    trening = models.ForeignKey(Turnir)
    user = models.ForeignKey(User)

class Transakcija(models.Model):
    user = models.ForeignKey(User)
    datumTransakcije = models.dateField()
    iznosUplate = models.DecimalField()