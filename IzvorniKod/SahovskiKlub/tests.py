from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .views.main_views import HomeView
from .views.prikazNovosti_view import NovostiView
from .models import Trening, DojavaPogreske, Turnir, Novost

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
        trening = Trening(organizator=self.user)
        self.assertEqual(trening.organizator.username, self.user.username)
        self.assertEqual(trening.vrijemePocetka, None)
        self.assertEqual(trening.vrijemeZavrsetka, None)

class UnitTreningTestFail(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = "korisnik123"

    def test_details(self):
        trening = Trening(organizator=self.user)



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
        novost = Novost(user_id=self.user.id)
        self.assertEqual(novost.user.username, self.user.username)
        self.assertEqual(novost.vrijemeObjave, None)
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
        self.assertEqual(turnir.organizator.username, self.user.username)
        self.assertEqual(turnir.vrijemePocetka, None)
        self.assertEqual(turnir.vrijemeZavrsetka, None)
        self.assertEqual(turnir.formatTurnira, '')
        self.assertTrue(type(self.brojSudionika) is int)