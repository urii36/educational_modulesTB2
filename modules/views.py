from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from modules.models import Module
from modules.pagination import ModulesPaginator
from modules.serializers import ModuleSerializer


class ModulesCreateAPIView(generics.CreateAPIView):
    """View to create a module"""
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_module = serializer.save()
        new_module.owner = self.request.user
        new_module.save()


class ModulesListAPIView(generics.ListAPIView):
    """View to get a list of modules"""
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    pagination_class = ModulesPaginator


class ModulesRetrieveAPIView(generics.RetrieveAPIView):
    """View to get a singe module by id"""
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsAuthenticated]


class ModulesUpdateAPIView(generics.UpdateAPIView):
    """View to edit a module by id"""
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Module.objects.filter(owner=self.request.user)


class ModulesDestroyAPIView(generics.DestroyAPIView):
    """View to delete a module by id"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Module.objects.filter(owner=self.request.user)
