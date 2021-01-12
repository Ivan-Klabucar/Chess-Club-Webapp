from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone
from .views.main_views import HomeView
from .views.taktika_views import TacticRevisionView
from .views.prikazNovosti_view import NovostiView
from .models import Trening, DojavaPogreske, Turnir, Novost, Profil, Taktika
import datetime

class RequestHomepageTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_details(self):
        print("Upisite korisnicko ime")
        username = input()
        print("Upisite lozinku")
        lozinka = input()
        request = self.factory.get('/')
        try:
            request.user = User.objects.create_user(
                username=username, email=username+'@fer.hr', password=lozinka)
        except ValueError:
            pass
        response = HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

class UnitTreningTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='trener', email='trener@fer.hr', password='top_secret')

    def test_details(self):
        vrijeme = datetime.datetime.now(tz=timezone.utc)
        trening = Trening(organizator=self.user, vrijemePocetka=vrijeme, vrijemeZavrsetka=vrijeme)
        trening.save()
        self.assertEqual(trening.organizator.username, self.user.username)
        self.assertEqual(trening.vrijemePocetka, vrijeme)
        self.assertEqual(trening.vrijemeZavrsetka, vrijeme)


class UnitTreningTestFail(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = "korisnik123"

    def test_details(self):
        vrijeme = datetime.datetime.now(tz=timezone.utc)
        trening = Trening(organizator=self.user)
        trening.save()



class RequestNovostiTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_details(self):
        print("Upisite korisnicko ime")
        username = input()
        print("Upisite lozinku")
        lozinka = input()
        request = self.factory.get('/novosti')
        try:
            request.user = User.objects.create_user(
                username=username, email=username + '@fer.hr', password=lozinka)
        except ValueError:
            pass
        response = NovostiView.as_view()(request)
        self.assertEqual(response.status_code, 200)

class UnitNovostiTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='trener', email='trener@fer.hr', password='top_secret')

    def test_details(self):
        vrijeme = datetime.datetime.now(tz=timezone.utc)
        novost = Novost(user_id=self.user.id, vrijemeObjave=vrijeme)
        novost.save()
        self.assertEqual(novost.user.username, self.user.username)
        self.assertEqual(novost.vrijemeObjave, vrijeme)
        self.assertEqual(novost.naslov, '')
        self.assertEqual(novost.tekst, '')

class UnitTurnirTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='trener', email='trener@fer.hr', password='top_secret')
        self.brojSudionika = 'deset'

    def test_details(self):
        turnir = Turnir(organizator=self.user, brojSudionika=self.brojSudionika)
        turnir.save()


class RequestTacticErrorReportToRightUserTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.normal_user = User.objects.create_user(
            username='John', email='john@hotmail.com', password='top_secret')
        self.trener = User.objects.create_user(
            username='trener', email='trener@hotmail.com', password='top_secret')
        self.trener.profil.trener = True

    def test_details(self):
        vrijeme = datetime.datetime.now(tz=timezone.utc)
        taktika = Taktika(ime="laka_taktika", createdAt=vrijeme, user=self.trener, initConfig="k7/8/8/8/5n2/8/8/1K3Q2 w KQkq - 0 1", movesWhite="Qh1+,Qe4,Qxf4", movesBlack="Ka7,Ka6", tezina=1, brojGlasova=1, validnost=True, vidljivost=True)
        taktika.save()
        dojava_pogreske = DojavaPogreske(taktika=taktika, userDojave=self.normal_user, userRevizija=self.trener, predlozeniTijek="Qf3+,Qxf4<W|B>Ka7", opis="vrlo informativan opis")
        dojava_pogreske.save()
        request = self.factory.get(f'/revidiranjeTaktike?id={dojava_pogreske.id}')
        request.user = self.trener
        response = TacticRevisionView.as_view()(request)
        self.assertEqual(response.status_code, 200)