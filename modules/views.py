from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from modules.models import Module
from modules.pagination import ModulesPaginator
from modules.serializers import ModuleSerializer


class ModulesCreateAPIView(generics.CreateAPIView):
    """View для создания модуля."""
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_module = serializer.save()
        new_module.owner = self.request.user
        new_module.save()


class ModulesListAPIView(generics.ListAPIView):
    """View для получения списка модулей."""
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    pagination_class = ModulesPaginator


class ModulesRetrieveAPIView(generics.RetrieveAPIView):
    """View для получения отдельного модуля по идентификатору."""
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsAuthenticated]


class ModulesUpdateAPIView(generics.UpdateAPIView):
    """View для редактирования модуля по идентификатору."""
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Module.objects.filter(owner=self.request.user)


class ModulesDestroyAPIView(generics.DestroyAPIView):
    """View для удаления модуля по идентификатору."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Module.objects.filter(owner=self.request.user)
