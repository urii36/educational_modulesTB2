from django.urls import path

from modules.views import ModulesCreateAPIView, ModulesListAPIView, ModulesRetrieveAPIView, ModulesUpdateAPIView, \
    ModulesDestroyAPIView

urlpatterns = [
    path('modules/create/', ModulesCreateAPIView.as_view(), name='module_create'),
    path('modules/', ModulesListAPIView.as_view(), name='modules'),
    path('modules/<int:pk>/', ModulesRetrieveAPIView.as_view(), name='module'),
    path('modules/update/<int:pk>/', ModulesUpdateAPIView.as_view(), name='module_update'),
    path('modules/delete/<int:pk>/', ModulesDestroyAPIView.as_view(), name='module_delete'),
]
