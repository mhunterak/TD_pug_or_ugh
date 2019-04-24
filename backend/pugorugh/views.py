from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import Http404

from rest_framework import permissions, mixins, status
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView)
from rest_framework.views import APIView, status
from rest_framework.response import Response
from django.db.models import Q

from django.shortcuts import get_object_or_404

from . import models
from . import serializers


def get_age_range(userPref_age):
    """
    Converts the database character ('b', 'a') into a range of numbers to
    select a dog by age
    """
    acceptable_ages = []
    ages = {
        'b': range(0, 13),
        'y': range(13, 25),
        'a': range(25, 60),
        's': range(60, 500),
    }
    userPrefList = userPref_age.split(',')
    if len(userPrefList):
        for agePref in userPrefList:
            try:
                for age in ages[agePref]:
                    acceptable_ages.append(age)
            except KeyError:
                pass
    if not len(acceptable_ages):
        for num in range(0, 500):
            acceptable_ages.append(num)
    return acceptable_ages


'''
# To get the next liked/disliked/undecided dog
'''


# /api/dog/<pk>/liked/next/
class LikedNext(APIView):
    '''
    This view gets the next dog that you've liked
    '''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        userPref = models.UserPref.objects.get(user__id=request.user.id)
        dogs = models.Dog.objects.all().filter(
            Q(userdog__status__in=('l')) &
            Q(userdog__user__id=request.user.id) &
            Q(id__gt=pk)
        )
        serializer = serializers.DogSerializer(dogs.first())

        return Response(serializer.data, status=status.HTTP_200_OK)


# /api/dog/<pk>/disliked/next/
class DislikedNext(APIView):
    '''
    This view gets the next dog that you've disliked
    '''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        dogs = models.Dog.objects.all().filter(
            Q(userdog__status__in=('d')) &
            Q(userdog__user__id=request.user.id) &
            Q(id__gt=pk)
        )
        serializer = serializers.DogSerializer(dogs.first())
        if dogs.first() is None:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


# /api/dog/<pk>/undecided/next/
class UndecidedNext(APIView):
    '''
    This view gets the next dog that you haven't decided on yet
    '''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None, *args, **kwargs):
        userPref = get_object_or_404(models.UserPref, user__id=request.user.id)
        dogs = models.Dog.objects.all().exclude(
            Q(userdog__status__in=('d', 'l'))).exclude(
            Q(userdog__user__id=request.user.id)).exclude(
            Q(id__lte=pk)
        ).filter(gender__in=userPref.gender
                 ).filter(size__in=userPref.size
                          ).filter(age__in=get_age_range(userPref.age))
        serializer = serializers.DogSerializer(dogs.first())
        if dogs.first() is None:
            return Response(serializer.data,
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)


# EXTRA CREDIT

# /api/dog/add/
class AddDog(mixins.UpdateModelMixin, CreateAPIView):
    '''
    # Extend the application by allowing
    # the {{addition}} or deletion of dogs to the site.
    '''
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = serializers.DogSerializer
    model = models.Dog

    def put(self, request, pk):
        self.check_permissions(clone_request(self.request, 'POST'))
        serializer = serializers.DogSerializer(
        )
        data = {
            'name': request.data['name'],
            'breed': request.data['breed'],
            'age': request.data['age'],
            'gender': request.data['gender'],
            'image_filename': request.data['image_filename'],
            'size': request.data['size'],
        }
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteDog(DestroyAPIView):
    '''
    # Extend the application by allowing
    # the addition or {{deletion}} of dogs to the site.
    '''
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = serializers.DogSerializer()

    def put(self, request, pk, format=None, *args, **kwargs):
        self.check_permissions(clone_request(self.request, 'DELETE'))
        dog = models.Dog.objects.get(id=pk)
        data = {
            'dog': pk,
        }
        serializer = serializers.DogSerializer(data=data)
        serializer.is_valid()
        serializer.delete(validated_data=data)
        return Response(serializer.data, status=status.HTTP_200_OK)


# /api/dog/<breed>/<pk>/undecided/next/
class UndecidedBreedNext(APIView):
    '''
    XC - Additional routes are added to site which
    increase the applications functionality.

    This view gets the next dog that you haven't decided on yet,
    with the breed you choose
    '''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, breed, pk, format=None, *args, **kwargs):
        userPref = get_object_or_404(models.UserPref, user__id=request.user.id)
        dogs = models.Dog.objects.all().exclude(
            Q(userdog__status__in=('d', 'l')) &
            Q(userdog__user__id=request.user.id)
        ).filter(gender__in=userPref.gender
                 ).filter(breed__icontains=breed
                          ).filter(size__in=userPref.size
                                   ).filter(age__in=get_age_range(userPref.age)
                                            ).filter(~Q(id=pk))
        serializer = serializers.DogSerializer(dogs.first())
        return Response(serializer.data, status=status.HTTP_200_OK)


'''
# To change the dog's status
'''


# /api/dog/<pk>/liked/
class Liked(mixins.UpdateModelMixin, CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserDogSerializer
    model = models.UserDog

    def put(self, request, pk):
        dog = models.Dog.objects.get(id=pk)
        data = {
            'status': 'l',
            'user': request.user.id,
            'dog': dog.id,
        }
        serializer = serializers.UserDogSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# /api/dog/<pk>/disliked/
class Disliked(mixins.CreateModelMixin, RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserDogSerializer
    model = models.UserDog

    def put(self, request, pk, format=None, *args, **kwargs):
        dog = models.Dog.objects.get(id=pk)
        data = {
            'status': 'd',
            'user': request.user.id,
            'dog': dog.id,
        }
        serializer = serializers.UserDogSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# /api/dog/<pk>/undecided/
class Undecided(DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserDogSerializer()
    model = models.UserDog

    def put(self, request, pk, format=None, *args, **kwargs):
        userdog = models.UserDog.objects.all().filter(
            dog__id=pk).filter(user__id=request.user.id)
        dog = models.Dog.objects.get(id=pk)
        data = {
            'user': request.user.id,
            'dog': dog.id,
        }
        serializer = serializers.UserDogSerializer(data=data)
        serializer.is_valid()
        serializer.delete(validated_data=data)
        return Response(serializer.data, status=status.HTTP_200_OK)


'''
# To change or set user preferences
'''


# /api/user/preferences/
class SetUserPref(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer
    model = models.UserPref
    lookup_field = 'userpref'

    def get(self, request, format=None, *args, **kwargs):
        print("userpref get")
        userPref = models.UserPref.objects.get(
            models.UserPref, user__id=request.user.id)
        if userPref is not None:
            serializer = serializers.UserPrefSerializer(userPref)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('User Preferences not set',
                            status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        self.check_permissions(clone_request(self.request, 'POST'))
        userPref = models.UserPref.get(models.UserPref,
                                       user=self.request.user)
        serializer = serializers.UserPrefSerializer(
            userPref, data=self.request.data)
        serializer.is_valid()
        if userPref is None:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        try:
            userPref = models.UserPref.objects.get(user=self.request.user)
            serializer = serializers.UserPrefSerializer(
                userPref,
                instance=userPref,
                data=self.request.data)

        except models.UserPref.DoesNotExist:
            data = {
                'user': request.user.id,
                'age': request.data['age'],
                'gender': request.data['gender'],
                'size': request.data['size'],
            }
            serializer = serializers.UserPrefSerializer(data=data)
            serializer.is_valid(data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# AUTH


class UserRegisterView(CreateAPIView):
    '''
    Let anyone register a new user account
    '''
    permission_classes = (permissions.AllowAny,)
    model = User
    serializer_class = serializers.UserSerializer
