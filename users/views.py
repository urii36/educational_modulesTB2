from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny


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
