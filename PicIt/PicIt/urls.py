"""PicIt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from webserviceapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test', views.pagina_de_prueba),
    path('publicaciones', views.mostrar_publicaciones),
    path('publicar/<int:id_tagSolicitado>', views.subir_publicacion),
    path('publicacion/<int:id_solicitado>', views.obtener_detalle_publicacion),
    path('publicacion/<int:publicacion_id>/like', views.dar_like),
    path('tags', views.obtener_tags),
    path('likes', views.obtener_like),
    path('crearCarp', views.crear_carpeta),
    path('carpeta', views.mostrar_carpetas),
    path('folders/<int:carpeta_id>', views.anadir_publicacion_carpeta),
    path('folders/<int:id_solicitado>/publicaciones', views.mostrar_publicaciones_carpeta),
    path('users', views.listar_amigos),
    path('editarDatos/<int:id_solicitado>', views.datos_editar),
    path('aplicarCambioDatos', views.aplicar_edicion),
    path('datosUsuario/<int:id_solicitado>', views.datos_user),
    path('seguidores/<int:id_solicitado>', views.seguidores),

    path('registro', views.registrarUsuario),
    path('login', views.sessions),
    path('usuarios/<int:usuario_id>/mensajes', views.enviar_mensaje),
    path('mensajes/<int:id_solicitado>', views.mostrar_mensajes_chat_concreto)
]
