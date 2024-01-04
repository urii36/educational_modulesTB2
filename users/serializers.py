from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    qty_modules = serializers.SerializerMethodField()

    def get_qty_modules(self, instance):
        """qty of user's modules"""
        return instance.module.count()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'birth_date', 'qty_modules')


class UserCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'birth_date')
