from django.contrib.auth.models import User

from rest_framework import serializers

from . import models


class DogSerializer(serializers.ModelSerializer):
    queryset = models.Dog.objects.all()

    def create(self, validated_data):
        dog = models.Dog.objects.create(
            name=validated_data['name'],
            age=validated_data['age'],
            gender=validated_data['gender'],
            image_filename=validated_data['image_filename'],
            size=validated_data['size'],
        ),
        try:
            dog = models.Dog.objects.filter(
                name=validated_data['name']).update(
                breed=validated_data['breed'],
            )
        except KeyError:
            pass

    class Meta:
        fields = (
            'id',
            'name',
            'breed',
            'age',
            'gender',
            'image_filename',
            'size',
        )
        model = models.Dog


class UserDogSerializer(serializers.ModelSerializer):
    queryset = models.UserDog.objects.all()

    def create(self, validated_data):
        userDog = models.UserDog.objects.create(
            **validated_data
        )
        return userDog

    def delete(self, validated_data):
        self.delete

    class Meta:
        model = models.UserDog
        fields = (
            'user',
            'dog',
            'status',
        )


class UserPrefSerializer(serializers.ModelSerializer):
    queryset = models.UserPref.objects.all()

    def create(self, validated_data):
        userPref = models.UserPref.objects.create(
            **validated_data
        )
        return userPref

    class Meta:
        model = models.UserPref
        fields = (
            'id',
            'user',
            'age',
            'gender',
            'size'
        )


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = '__all__'
