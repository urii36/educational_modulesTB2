from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    qty_modules = serializers.SerializerMethodField()

    def get_qty_modules(self, instance):
        """Kол-во пользовательских модулей."""
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


class UserLoginSerializer(serializers.Serializer):
    """
        Сериализатор для аутентификации пользователя.

        Attributes:
            email (str): Адрес электронной почты пользователя.
            password (str): Пароль пользователя.

        Methods:
            validate(data): Проверяет переданные данные на наличие
                корректных учетных данных пользователя.

        Raises:
            serializers.ValidationError: Если учетные данные некорректны или отсутствуют.

        Returns:
            dict: Словарь с проверенными данными, включая объект пользователя (если успешно).
    """
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            print(user)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data
