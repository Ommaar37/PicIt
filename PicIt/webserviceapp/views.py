from django.shortcuts import render
from django.http import HttpResponse
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
		diccionario['titulo']= fila_sql.Titulo
		diccionario['Imagen']= fila_sql.Imagen
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)


def obtener_detalle_publicacion(request, id_solicitado):
	publicacion = Publicaciones.objects.get(id = id_solicitado)
	resultado = {
		'id':publicacion.id,
		'titulo': publicacion.Titulo,
		'imagen': publicacion.Imagen,
		'descripcion': publicacion.Descripcion,
		'tags': publicacion.Tags,
		'fecha': publicacion.Fecha
	}
	return JsonResponse(resultado, json_dumps_params={'ensure_ascii':False});
	
def subir_publicacion(request):
	if request.method !='POST':
		return None
	tokenRecibido = request.headers.get('Auth-Token')
	json_peticion = json.loads(request.body)
	publicacion = Publicaciones()
	publicacion.Titulo = json_peticion['titulo_publicacion']
	publicacion.Imagen = json_peticion['imagen_publicacion']
	publicacion.Descripcion = json_peticion['descripcion_publicacion']
	publicacion.Tags = json_peticion['tags_publicacion']
	publicacion.Fecha = json_peticion['fecha_publicacion']
	publicacion.save()
	return JsonResponse({"status": "ok"})

def obtener_tags(request):
	lista= Tags.objects.all()
	respuesta_final=[]
	
	for fila_sql in lista:
		diccionario = {}
		diccionario['tag'] = fila_sql.Nombre
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
	like.idUser = Usuarios.objects.get(token = tokenRecibido)
	respuesta_final = []
	
	for fila_sql in lista:
		diccionario={}
		diccionario['publicacion']= fila_sql.idPublic
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe = False)

def crear_carpeta (request):
	if request.method != ‘POST’:
		return None
	
	json_peticion = json.loads(request.body)
	folder = Folders()
	folder.folder = json_peticion[‘nueva_carpeta’]
	carpeta.publicacion = Publicaciones.objects.get(id = IdPublicacion)
	carpeta.save()
	return JsonResponse({“status”: “ok”})

def mostrar_carpetas (request):
	lista = folders.objects.all()
	respuesta_final = []
	for fila_sql in lista:
		diccionario = {}
		diccionario[‘Id’] = fila_sql.Id
		diccionario[‘Name’] = fila_sql.Name
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)

def anadir_publicacion_carpeta (request, carpeta_id):
	if request.method != ‘PATCH’:
		return None
	
	json_peticion = json.loads(request.body)
	post = Posts()
	post.Posts = json_peticion[‘nueva_publicacion’]
	carpeta.publicacion = Publicaciones.objects.get(id = IdPublicacion)
	comentario.save()
	return JsonResponse({“status”: “ok”})

def mostrar_publicaciones_carpeta (request, id_solicitado):
	carpeta = Folders.object.get(id = id_solicitado)
	publicaciones = carpeta.Publicaciones_set.all()
	lista_publicaciones = []
	for fila_publicaciones_sql in publicaciones:
		diccionario = {}
		diccionario[‘Id’] = fila_publicaciones_sql.Id
		diccionario[‘Imagen’] = fila_publicaciones_sql.Imagen
		diccionario[‘Titulo’] = fila_publicaciones_sql.Titulo
		diccionario[‘Descripción’] = fila_publicaciones_sql.Descripción
		diccionario[‘Fecha’] = fila_publicaciones_sql.Fecha
		lista_publicaciones.append(diccionario)
	resultado = {
		‘Id’: carpeta.Id,
		‘Nombre’: carpeta.Nombre,
		‘Publicaciones’: carpeta.lista_publicaciones
	}
	
	return JsonResponse(resultado, json_dimps_params={‘ensure_ascii’: False})

def listar_amigos (request):
	lista = friends.objects.all()
	respuesta_final = []
	for fila_sql in lista:
		diccionario = {}
		diccionario[‘Username’] = fila_sql.Username
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)

def enviar_mensaje (request):
	if request.method != ‘POST’:
		return None
	
	json_peticion = json.loads(request.body)
	message = Messages()
	message.message = json_peticion[‘nuevo_mensaje’]
	message.user = Publicaciones.objects.get(id = idUser)
	message.save()
	return JsonResponse({“status”: “ok”})

def mostrar_mensajes_chat_concreto (request, id_solicitado):
	usuario = Users.object.get(id = id_solicitado)
	mensaje = usuario.Mensajes_set.all()
	lista_mensajes = []
	for fila_mensajes_sql in mensajes:
		diccionario = {}
		diccionario[‘Id’] = fila_publicaciones_sql.Id
		diccionario[‘Mensaje’] = fila_publicaciones_sql.Mensaje
		diccionario[‘Fecha’] = fila_publicaciones_sql.Fecha
		lista_mensajes.append(diccionario)
	resultado = {
		‘Id’: carpeta.Id,
		‘Username’: carpeta.Username,
		‘Mensajes’: usuario.lista_mensajes
	}
	
	return JsonResponse(resultado, json_dimps_params={‘ensure_ascii’: False})
