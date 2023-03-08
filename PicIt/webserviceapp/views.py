from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Publicaciones, PublicCarpetas, Usuarios, Tags, Likes, Carpetas, Mensaje, Follow
import json
import jwt
from json import JSONDecodeError
from datetime import date
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def pagina_de_prueba(request):
	return HttpResponse("<h1>Hola caracola</h1>");

@csrf_exempt
def registrarUsuario(request):
    if request.method == 'POST':
        try:
            json_peticion = json.loads(request.body)
            usuario = Usuarios()
            usuario.nombreuser = json_peticion['username']
            usuario.email = json_peticion['email']
            usuario.contrasena = json_peticion['password']
            if usuario.nombreuser == '' or usuario.email == '' or usuario.contrasena == '':
                return JsonResponse({"status": "Faltan parámetros"}, status=400)
            else:
                if Usuarios.objects.filter(nombreuser=usuario.nombreuser).exists():
                    return JsonResponse({"status": "Nombre de usuario ya existente"}, status=409)
                else:
                    if Usuarios.objects.filter(email=usuario.email).exists():
                        return JsonResponse({"status": "Email ya existente"}, status=409)
                    else:
                        usuario.set_password(json_peticion['password'])
                        payload = {
                            'NombreUsuario': usuario.nombreuser,
                            'Email': usuario.email
                        }
                        secret = 'abc123'
                        token = jwt.encode(payload, secret, algorithm='HS256')
                        usuario.tokensession = token
                        usuario.save()
                        return JsonResponse({"status": "ok"}, status=201)
        except (JSONDecodeError, Exception):
            return JsonResponse({"status": "Error"})

@csrf_exempt
def sessions(request):
    if request.method == "POST":
        user = Usuarios()
        try:
            json_peticion = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "Bad request"}, status=400)
        try:
            user = Usuarios.objects.get(email=json_peticion["email"])
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Not found"}, status=404)
        contrasena = json_peticion["password"]
        user.set_password(contrasena)
        if check_password(contrasena, user.contrasena):
            payload = {
                'NombreUser': user.nombreuser,
                'Email': user.email
            }
            secret = 'abc123'
            token = jwt.encode(payload, secret, algorithm='HS256')
            user.token = token
            user.save()
            return JsonResponse({"sessionToken": token}, status=200)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

@csrf_exempt
def enviar_mensaje (request, usuario_id):
        if request.method == 'POST':
            json_peticion = json.loads(request.body)
            mensajes = Mensaje()
            mensajes.mensaje = json_peticion['nuevo_mensaje']
            mensajes.iduser = Usuarios.objects.get(id=usuario_id)
            mensajes.fecha = date.today()
            mensajes.save()
            return JsonResponse({'status': 'ok'})

@csrf_exempt
def mostrar_mensajes_chat_concreto (request, id_solicitado):
        usuario = Usuarios.objects.get(id = id_solicitado)
        mensajes = usuario.mensaje_set.all()
        lista_mensajes = []
        for fila_mensajes_sql in mensajes:
                diccionario = {}
                diccionario['id'] = fila_mensajes_sql.id
                diccionario['mensaje'] = fila_mensajes_sql.mensaje
                diccionario['fecha'] = fila_mensajes_sql.fecha
                lista_mensajes.append(diccionario)
        resultado = {
                'id': usuario.id,
                'username': usuario.nombreuser,
                'mensajes': lista_mensajes
        }
        return JsonResponse(resultado, json_dumps_params={'ensure_ascii': False})

#------------------------------------------------------------------------------------------------

#OMAR--GET QUE OBTIENE LAS PUBLICACIONES SUBIDAS.
@csrf_exempt
def mostrar_publicaciones(request):
	lista=Publicaciones.objects.all()
	respuesta_final = []
	
	for fila_sql in lista:
		diccionario={}
		diccionario['titulo']= fila_sql.titulo
		diccionario['Imagen']= fila_sql.imagen
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)

#OMAR--POST QUE SIRVE PARA DARLE LIKES A PUBLICACIONES
@csrf_exempt
def dar_like(request, publicacion_id):
	if request.method !='PUT':
		return None
	tokenRecibido  = request.headers.get('Auth-Token')
	like = Likes()
	like.iduser =  Usuarios.objects.get(tokensession= tokenRecibido)
	like.idpublic = Publicaciones.objects.get(id =  publicacion_id)
	like.save()
	return JsonResponse({"status": "ok"})

#OMAR--GET QUE OBTIENE EL NÚMERO DE LIKES DADOS A UN USER EN CONCRETO.
@csrf_exempt
def obtener_like(request):
	lista=Likes.objects.all()
	tokenRecibido = request.headers.get('Auth-Token')
	like.idUser = Usuarios.objects.get(tokensession = tokenRecibido)
	respuesta_final = []
	if not tokenRecibido or tokenRecibido != tokensession: 
		return JsonResponse({'error':'Invalid token'}, status=400)
	for fila_likes_sql in lista:
		diccionario={}
		diccionario['publicacion']= fila_sql.idPublic
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe = False)

#OMAR--POST QUE CREA CARPETA
@csrf_exempt
def crear_carpeta (request):
	#COMPROBACIÓN DEL MÉTODO
	if request.method != 'POST':
		return None
	TokenRecibido = request.headers.get('Auth-Token')
	json_peticion = json.loads(request.body)
	carpeta = Carpetas()
	carpeta.nombre = json_peticion['nueva_carpeta']
	aux = Usuarios.objects.get(tokensession = TokenRecibido)
	carpeta.iduser = aux
	carpeta.save()
	return JsonResponse({'status': 'ok'})

#OMAR--GET QUE OBTIENE LOS DATOS DE CADA CARPETA Y LO MUESTRA
@csrf_exempt
def mostrar_carpetas (request):
	lista=Carpetas.objects.all()
	respuesta_final = []
	for fila_carpetas_sql in lista:
		diccionario = {}
		diccionario['Id'] = fila_carpetas_sql.id
		diccionario['Nombre'] = fila_carpetas_sql.nombre
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)

#OMAR--GET QUE OBTIENE LOS DATOS DE UNA CARPETA, SACA CADA IMAGEN, CADA TITULO, CADA DESC Y FECHA
@csrf_exempt
def mostrar_publicaciones_carpeta (request, id_solicitado):
	carpeta = Carpetas.objects.get(id = id_solicitado)
	publicacion = carpeta.Publicaciones_set.all()
	lista_publicaciones = []
	for fila_publicaciones_sql in publicacion:
		diccionario = {}
		diccionario['Id'] = fila_publicaciones_sql.id
		diccionario['Imagen'] = fila_publicaciones_sql.imagen
		diccionario['Titulo'] = fila_publicaciones_sql.titulo
		diccionario['Descripción'] = fila_publicaciones_sql.descripcion
		diccionario['Fecha'] = fila_publicaciones_sql.fecha
		lista_publicaciones.append(diccionario)
	resultado = {
		'Id': carpeta.id,
		'Nombre': carpeta.nombre,
		'Publicaciones': carpeta.lista_publicaciones
	}
	
	return JsonResponse(resultado, json_dimps_params={'ensure_ascii': False})


#ELENA--GET QUE OBTIENE LOS DETALLES DE UNA PUBLICACIÓN AL QUE SE LE PASA EL ID DE LA MISMA
@csrf_exempt
def obtener_detalle_publicacion(request, id_solicitado):
	publicacion = Publicaciones.objects.get(id = id_solicitado)
	resultado = {
		'id':publicacion.id,
		'titulo': publicacion.titulo,
		'imagen': publicacion.imagen,
		'descripcion': publicacion.descripcion,
		'fecha': publicacion.fecha
	}
	return JsonResponse(resultado, json_dumps_params={'ensure_ascii':False});

#ELENA--POST QUE SUBE LAS PUBLICACIONES DÁNDOLES UN ID, LE HAY QUE INTRODUCIR TITULO, IMAGEN, DESCRIPCIÓN Y TAMBIÉN SE LE DA FECHA
@csrf_exempt
def subir_publicacion(request, id_tagSolicitado):
	if request.method !='POST':
		return None
	tokenRecibido = request.headers.get('Auth-Token')
	json_peticion = json.loads(request.body)
	publicacion = Publicaciones()
	publicacion.iduser = Usuarios.objects.get(tokensession = tokenRecibido)
	publicacion.titulo = json_peticion['titulo_publicacion']
	publicacion.imagen = json_peticion['imagen_publicacion']
	publicacion.descripcion = json_peticion['descripcion_publicacion']
	publicacion.idtag = Tags.objects.get(id = id_tagSolicitado)
	publicacion.fecha = json_peticion['fecha_publicacion']
	publicacion.save()
	return JsonResponse({"status": "ok"})

#ELENA--MÉTODO GET QUE OBTIENE LOS TAGS
@csrf_exempt
def obtener_tags(request):
	lista= Tags.objects.all()
	respuesta_final=[]
	
	for fila_tags_sql in lista:
		diccionario = {}
		diccionario['Nombre'] = fila_tags_sql.nombre
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)



#ELENA--PATCH QUE AÑADE UNA PUBLICACIÓN (UTILIZANDO SU ID) A UNA CARPETA DETERMINADA (UTILIZANDO SU ID)
@csrf_exempt
def anadir_publicacion_carpeta (request, carpeta_id):
	#COMPROBACIÓN DEL MÉTODO
	if request.method != 'PATCH':
		return None
	publicacion = Publicaciones()
	json_peticion = json.loads(request.body)
	publicacionCarpeta = PublicCarpetas()
	publicacionCarpeta.idpublic = Publicaciones.objects.get(id = json_peticion['publicacion_id'])
	publicacionCarpeta.idcarpeta = Carpetas.objects.get(id = carpeta_id)
	publicacionCarpeta.save()
	return JsonResponse({'status': 'ok'})


#ELENA--GET OBTIENE LOS SEGUIDORES DE UN USUARIO
@csrf_exempt
def seguidores(request, id_solicitado):
	datos = Follow.objects.get(idseguido = id_solicitado)
	tokenRecibido = request.headers.get('Auth-Token')
	datos.idseguido = Usuarios.objects.get(tokensession = tokenRecibido)
	resultado = {
		'idSeguidor': count(datos.idseguidor)
	}
	return JsonResponse(resultado, json_dumps_params={'ensure_ascii': False})

#ELENA--GET QUE OBTIENE LOS SEGUIDOS
@csrf_exempt
def seguidos(request, id_solicitado):
	usuario = Usuarios.objects.get(id = id_solicitado)
	datos = Follow.objects.get(idseguido = usuario.id)
	tokenRecibido = request.headers.get('Auth-Token')
	datos.idseguido = Usuarios.objects.get(tokensession = tokenRecibido)
	resultado = {
		'idSeguidor':count( datos.idseguido)
	}
	return JsonResponse(resultado, json_dumps_params={'ensure_ascii': False})

#BET--GET QUE OBTIENE LOS AMIGOS PARA DETERMINADO USER
@csrf_exempt
def listar_amigos (request):
	lista = Follow.objects.all()
	tokenRecibido = request.headers.get('Auth-Token')
	lista.idseguido = Usuarios.objects.get(tokensession = tokenRecibido)
	respuesta_final = []
	for fila_sql in lista:
		diccionario = {}
		diccionario['Username'] = fila_sql.username
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)

#BET--GET QUE OBTIENE LOS DATOS EDITABLES DENTRO DE UN USER
@csrf_exempt
def datos_editar(request, id_solicitado):
	datos = Usuarios.objects.get(id = id_solicitado)
	resultado = {
		'Nombre': datos.nombre,
		'NombreUser': datos.nombreuser,
		'Email': datos.email,
		'Contrasena': datos.contrasena,
		'Genero': datos.genero,
		'Pais': datos.pais,
		'biografia': datos.biografia,
		'Apellidos': datos.apellidos
	}
	return JsonResponse(resultado, json_dumps_params={'ensure_ascii':False});

#BET--POST PARA APLICAR LOS CAMBIOS REALIZADOS A NUESTRO USER
@csrf_exempt
def aplicar_edicion(request):
	if request.method !='POST':
		return None
	tokenRecibido = request.headers.get('Auth-Token')
	json_peticion = json.loads(request.body)
	usuario = Usuarios()
	usuario.Nombre = json_peticion['name']
	usuario.Apellidos = json_peticion['username']
	usuario.User = json_peticion['user']
	usuario.Email = json_peticion['email']
	usuario.Contraseña = json_peticion['password']
	usuario.Edad = json_peticion['edad']
	usuario.Genero = json_peticion['genero']
	usuario.Pais = json_peticion['pais']
	usuario.Biografia = json_peticion['biografia']
	usuario.save()
	return JsonResponse({"status": "ok"})

#BET--GET QUE OBTIENE LOS DATOS DE UN USER
@csrf_exempt
def datos_user(request, id_solicitado):
	datos = Usuarios.objects.get(id = id_solicitado) 
	resultado = {
		'Nombre': datos.nombre,
		'NombreUser': datos.nombreuser
	}
	return JsonResponse(resultado, json_dumps_params={'ensure_ascii':False});


