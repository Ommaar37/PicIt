from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Publicaciones, Usuarios, Tags, Likes
import json
# Create your views here.
@csrf_exempt
def pagina_de_prueba(request):
	return HttpResponse("<h1>Hola caracola</h1>");

def mostrar_publicaciones(request):
	lista=Publicaciones.objects.all()
	respuesta_final = []
	
	for fila_sql in lista:
		diccionario={}
		diccionario['titulo']= fila_sql.titulo
		diccionario['Imagen']= fila_sql.imagen
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)


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
	
def subir_publicacion(request):
	if request.method !='POST':
		return None
	tokenRecibido = request.headers.get('Auth-Token')
	json_peticion = json.loads(request.body)
	publicacion = Publicaciones()
	publicacion.titulo = json_peticion['titulo_publicacion']
	publicacion.imagen = json_peticion['imagen_publicacion']
	publicacion.descripcion = json_peticion['descripcion_publicacion']
	publicacion.tags = json_peticion['tags_publicacion']
	publicacion.fecha = json_peticion['fecha_publicacion']
	publicacion.save()
	return JsonResponse({"status": "ok"})

def obtener_tags(request):
	lista= Tags.objects.all()
	respuesta_final=[]
	
	for fila_tags_sql in lista:
		diccionario = {}
		diccionario['Nombre'] = fila_sql.nombre
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)


def dar_like(request, publicacion_id):
	if request.method !='PUT':
		return None
	tokenRecibido  = request.headers.get('Auth-Token')
	like = Likes()
	like.idUser =  Usuarios.objects.get(tokensession= tokenRecibido)
	like.idPublic = Publicaciones.objects.get(id =  publicacion_id)
	like.save()
	return JsonResponse({"status": "ok"})

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

def crear_carpeta (request):
	if request.method != 'POST':
		return None
	
	json_peticion = json.loads(request.body)
	folder = Folders()
	folder.folder = json_peticion['nueva_carpeta']
	carpeta.publicacion = Publicaciones.objects.get(id = IdPublicacion)
	carpeta.save()
	return JsonResponse({'status': 'ok'})

def mostrar_carpetas (request):
	lista = Carpetas.objects.all()
	respuesta_final = []
	for fila_sql in lista:
		diccionario = {}
		diccionario['Id'] = fila_sql.id
		diccionario['Name'] = fila_sql.name
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)

def anadir_publicacion_carpeta (request, carpeta_id):
	if request.method != 'PATCH':
		return None
	
	json_peticion = json.loads(request.body)
	post = Posts()
	post.Posts = json_peticion['nueva_publicacion']
	carpeta.publicacion = Publicaciones.objects.get(id = IdPublicacion)
	comentario.save()
	return JsonResponse({'status': 'ok'})

def mostrar_publicaciones_carpeta (request, id_solicitado):
	carpeta = Folders.object.get(id = id_solicitado)
	publicaciones = carpeta.Publicaciones_set.all()
	lista_publicaciones = []
	for fila_publicaciones_sql in publicaciones:
		diccionario = {}
		diccionario['Id'] = fila_publicaciones_sql.id
		diccionario['Imagen'] = fila_publicaciones_sql.imagen
		diccionario['Titulo'] = fila_publicaciones_sql.titulo
		diccionario['Descripción'] = fila_publicaciones_sql.descripción
		diccionario['Fecha'] = fila_publicaciones_sql.fecha
		lista_publicaciones.append(diccionario)
	resultado = {
		'Id': carpeta.id,
		'Nombre': carpeta.nombre,
		'Publicaciones': carpeta.lista_publicaciones
	}
	
	return JsonResponse(resultado, json_dimps_params={'ensure_ascii': False})

def listar_amigos (request):
	lista = friends.objects.all()
	respuesta_final = []
	for fila_sql in lista:
		diccionario = {}
		diccionario['Username'] = fila_sql.username
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)

def enviar_mensaje (request):
	if request.method != 'POST':
		return None
	
	json_peticion = json.loads(request.body)
	message = Messages()
	message.message = json_peticion['nuevo_mensaje']
	message.user = Publicaciones.objects.get(id = idUser)
	message.save()
	return JsonResponse({'status': 'ok'})

def mostrar_mensajes_chat_concreto (request, id_solicitado):
	usuario = Usuarios.object.get(id = id_solicitado)
	mensaje = usuario.Mensajes_set.all()
	lista_mensajes = []
	for fila_mensajes_sql in mensajes:
		diccionario = {}
		diccionario['Id'] = fila_publicaciones_sql.id
		diccionario['Mensaje'] = fila_publicaciones_sql.mensaje
		diccionario['Fecha'] = fila_publicaciones_sql.fecha
		lista_mensajes.append(diccionario)
	resultado = {
		'Id': carpeta.id,
		'Username': carpeta.username,
		'Mensajes': usuario.lista_mensajes
	}
	
	return JsonResponse(resultado, json_dimps_params={'ensure_ascii': False})
