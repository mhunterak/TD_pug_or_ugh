import json
from os import path

from django.test import TestCase, Client
from rest_framework.test import (
    APITestCase, APIRequestFactory, force_authenticate)

from . import models
from . import serializers
from . import views


# Create your tests here.


class PugOrUghTests(APITestCase):
    def setUp(self):
        PROJ_DIR = path.dirname(path.dirname(path.abspath(__file__)))
        filepath = path.join(PROJ_DIR, 'pugorugh', 'static',
                             'dog_details.json')
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            serializer = serializers.DogSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()

        self.user = models.User.objects.create_superuser(
            'testAdmin', 'ad@min.com', 'adminpassword')
        self.factory = APIRequestFactory()
        self.user = models.User.objects.get(username='testAdmin')
        self.user.userPref = models.UserPref.objects.create(user=self.user)

    def test_A(self):
        view = views.UserRegisterView.as_view()
        request = self.factory.post('/api/user/login/',
                                    {'username': 'adminTest',
                                     'password': 'admin123'})
        user = views.User.objects.all().first()
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_AA(self):
        view = views.SetUserPref.as_view()
        request = self.factory.put('/api/user/preferences/',
                                   {'age': 'b,y', 'gender': 'm,f', 'size': 's,xl'})
        user = views.User.objects.all().first()
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_B(self):
        view = views.UndecidedNext.as_view()
        request = self.factory.get('/api/dog/-1/undecided/next/')
        user = views.User.objects.all().first()
        force_authenticate(request, user=user)
        response = view(request, pk=-1)
        response.render()

        self.assertEqual(response.status_code, 200)
