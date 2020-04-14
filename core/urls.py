from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from auth.views import LoginViewSet, CreateUserViewSet, LogoutViewSet
from api.views import (AgendasViewSet, ConsultasViewSet, EspecialidadesViewSet,
                       MedicosViewSet)

router = routers.DefaultRouter()

router.register(r'medicos', MedicosViewSet)
router.register(r'especialidades', EspecialidadesViewSet)
router.register(r'agendas', AgendasViewSet)
router.register(r'consultas', ConsultasViewSet)
router.register(r'register', CreateUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', LoginViewSet.as_view()),
    path('logout/', LogoutViewSet.as_view())
]
