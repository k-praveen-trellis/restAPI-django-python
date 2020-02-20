from django.contrib import admin
from django.urls import path,include
from core.views import UserViewSet, ProfessionViewSet, DocumentViewSet,DatasheetViewSet
from rest_framework import routers
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'customers',UserViewSet,basename="customer")
router.register(r'professions',ProfessionViewSet)
router.register(r'documents',DocumentViewSet)
router.register(r'datasheets',DatasheetViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('api-auth/',include('rest_framework.urls')),
    path('api-token-auth/',views.obtain_auth_token)
]
