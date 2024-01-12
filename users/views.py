from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from django.contrib.auth import login


class UserViewSet(ModelViewSet):
    """Просмотр задан для модели пользователя. Для создания необходимо ввести "email" и "пароль". """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def get_permissions(self):
        if self.action != 'create':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class UserLoginViewSet(ViewSet):
    """
        Представление (ViewSet) для аутентификации пользователя и создания токена.

        Attributes:
            serializer_class (UserLoginSerializer): Класс сериализатора для аутентификации.

        Methods:
            create(request, *args, **kwargs): Метод для обработки запроса на аутентификацию пользователя,
                создания токена и возврата данных пользователя вместе с токеном.

        Returns:
            Response: Ответ, содержащий токен и данные пользователя.
    """
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        token, created = Token.objects.get_or_create(user=user)

        user_serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)
