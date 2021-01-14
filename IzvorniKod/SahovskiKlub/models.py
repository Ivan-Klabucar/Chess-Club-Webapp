from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_pgviews import view as pg

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    placenaClanarina = models.BooleanField(default=0)
    zabranjenPristup = models.BooleanField(default=0)
    trener = models.BooleanField(default=0)
    admin = models.BooleanField(default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profil.save()

class Taktika(models.Model):
    ime = models.CharField(max_length=50, default='default ime')
    createdAt = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    initConfig = models.CharField(max_length=100)
    movesWhite = models.CharField(max_length=3000)
    movesBlack = models.CharField(max_length=3000)
    tezina = models.DecimalField(max_digits=5, decimal_places=2)
    brojGlasova = models.IntegerField()
    validnost = models.BooleanField(default=1)
    vidljivost = models.BooleanField(default=1)

class RjesenjeTaktike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taktika = models.ForeignKey(Taktika, on_delete=models.CASCADE)
    vrijeme = models.DecimalField(max_digits=5, decimal_places=2)

RANG_LISTA_SQL = """
SELECT public."auth_user".username AS username, 
	   public."auth_user".id AS user_id,
       public."auth_user".id AS id,
	   ROUND(SUM(60 * public."SahovskiKlub_taktika".tezina * public."SahovskiKlub_taktika".tezina * 100 / public."SahovskiKlub_rjesenjetaktike".vrijeme)) AS bodovi
FROM public."SahovskiKlub_rjesenjetaktike"
	 JOIN public."auth_user" ON public."auth_user".id = public."SahovskiKlub_rjesenjetaktike".user_id
	 JOIN public."SahovskiKlub_taktika" ON public."SahovskiKlub_rjesenjetaktike".taktika_id = public."SahovskiKlub_taktika".id
GROUP BY public."auth_user".username, public."auth_user".id
ORDER BY SUM(public."SahovskiKlub_rjesenjetaktike".vrijeme * public."SahovskiKlub_taktika".tezina) DESC;
"""

class Bodovi(pg.View):
    username = models.CharField(max_length=150)
    user_id = models.IntegerField()
    bodovi = models.IntegerField()

    sql = RANG_LISTA_SQL

    class Meta:
        app_label = 'SahovskiKlub'
        db_table = 'sahovskiklub_bodovi'
        managed = False

class DojavaPogreske(models.Model):
    taktika = models.ForeignKey(Taktika, on_delete=models.CASCADE)
    userDojave = models.ForeignKey(User, on_delete=models.CASCADE)
    userRevizija = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userDojave')
    prihvacena = models.BooleanField(null=True, blank=True)
    predlozeniTijek = models.CharField(max_length=6000, default='')
    opis = models.CharField(max_length=3000, default='')

class RangLista(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bodovi = models.IntegerField()

class Novost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vrijemeObjave = models.DateTimeField()
    naslov = models.CharField(max_length=100, default='')
    tekst = models.CharField(max_length=3000, default='')
    vidljivost = models.BooleanField(default=1)

class Trening(models.Model):
    ime = models.CharField(max_length=50, default='default ime')
    organizator = models.ForeignKey(User, on_delete=models.CASCADE)
    vrijemePocetka = models.DateTimeField()
    vrijemeZavrsetka = models.DateTimeField()
    opisTreninga = models.CharField(max_length=100, default='')
    vidljivost = models.BooleanField(default=1)

class PrijavaTrening(models.Model):
    trening = models.ForeignKey(Trening, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Turnir(models.Model):
    ime = models.CharField(max_length=50, default='default ime')
    organizator = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    formatTurnira = models.CharField(max_length=100, default='')
    vrijemePocetka = models.DateTimeField()
    vrijemeZavrsetka = models.DateTimeField()
    brojSudionika = models.IntegerField()
    vidljivost = models.BooleanField(default=1)

class PrijavaTurnir(models.Model):
    turnir = models.ForeignKey(Turnir, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Transakcija(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datumTransakcije = models.DateField()
    iznosUplate = models.DecimalField(max_digits=5, decimal_places=2)

class Aktivnost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vrijemeAktivnosti = models.DateTimeField()
    aktivnost = models.CharField(max_length=100, default='')
