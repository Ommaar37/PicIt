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
