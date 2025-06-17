from tkinter.font import names

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import SolicitudesViewSet, modificar_solicitud, eliminar_solicitud, eliminar_consulta, ConsultasViewSet

#declaro el router y los endpoints
router = DefaultRouter()
router.register(r'Solicitudes', SolicitudesViewSet)
router.register(r'Consultas', ConsultasViewSet)

urlpatterns = [
    path('', views.pagina_index, name='index'), # path para el index
    path('simulador/', views.pagina_simulador, name='simulador'), #path para el formulario de simular credito hipotecario
    path('contacto/', views.pagina_contacto, name= 'contacto'), #path para el formulario de contacto
    path('dashboard/', views.dashboard, name= 'dashboard'), #path para el dashboard
    path('dashboard/solicitudes/', views.pagina_solicitudes, name= 'solicitudes'), #path para el el panel de solicitudes
    path('dashboard/consultas/', views.pagina_consultas, name= 'consultas'), #path para el panel de consultas
    path('modificarSolicitud/<int:solicitud_id>/', modificar_solicitud, name='modificar_solicitud'),# path para modificar solicitudes
    path('eliminarSolicitud/<int:solicitud_id>/', eliminar_solicitud, name='eliminar_solicitud'),# path para eliminar solicitudes
    path('eliminarConsulta/<int:consulta_id>/', eliminar_consulta, name='eliminar_consulta'),# path para eliminar consultas
    path('login/', auth_views.LoginView.as_view(template_name='simulador/login.html'), name='login'), #path para el login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), #path para el logout
    path('api/', include(router.urls)), #path para exponer los endpoints con el router
]