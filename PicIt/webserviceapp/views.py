from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Publicaciones, PublicCarpetas, Usuarios, Tags, Likes, Carpetas, Mensaje, Follow
import json
import jwt
from json import JSONDecodeError
from django.contrib.auth.hashers import check_password

# Create your views here.
@csrf_exempt
def pagina_de_prueba(request):
	return HttpResponse("<h1>Hola caracola</h1>");
#OMAR--GET QUE OBTIENE LAS PUBLICACIONES SUBIDAS.
def mostrar_publicaciones(request):
	lista=Publicaciones.objects.all()
	respuesta_final = []
	
	for fila_sql in lista:
		diccionario={}
		diccionario['titulo']= fila_sql.titulo
		diccionario['Imagen']= fila_sql.imagen
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)

#ELENA--GET QUE OBTIENE LOS DETALLES DE UNA PUBLICACIÓN AL QUE SE LE PASA EL ID DE LA MISMA
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
def obtener_tags(request):
	lista= Tags.objects.all()
	respuesta_final=[]
	
	for fila_tags_sql in lista:
		diccionario = {}
		diccionario['Nombre'] = fila_tags_sql.nombre
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)

#ELENA--POST QUE SIRVE PARA DARLE LIKES A PUBLICACIONES
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

#ELENA--POST QUE CREA CARPETA
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
def mostrar_carpetas (request):
	lista=Carpetas.objects.all()
	respuesta_final = []
	for fila_carpetas_sql in lista:
		diccionario = {}
		diccionario['Id'] = fila_carpetas_sql.id
		diccionario['Nombre'] = fila_carpetas_sql.nombre
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

#OMAR--GET QUE OBTIENE LOS DATOS DE UNA CARPETA, SACA CADA IMAGEN, CADA TITULO, CADA DESC Y FECHA
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

#BET--GET QUE OBTIENE LOS AMIGOS PARA DETERMINADO USER
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

#BET--POST QUE ENVÍA MENSAJE A LA BASE DED DATOS MENSAJE, TAMBIÉN GUARDA EL USER
def enviar_mensaje (request):
	#COMPROBACIÓN DEL MÉTODO
	if request.method != 'POST':
		return None
	
	json_peticion = json.loads(request.body)
	message = Messages()
	message.message = json_peticion['nuevo_mensaje']
	message.user = Publicaciones.objects.get(id = idUser)
	message.save()
	return JsonResponse({'status': 'ok'})

#BET--GET QUE RECUPERA LOS MENSAJES DEL CHAT
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

#BET--POST QUE REGISTRA LOS USUARIOS Y LOS AÑADE DENTRO DE LA  BASE DE DATOS
@csrf_exempt
def registrarUsuario(request):
	#COMPROBACIÓN DEL MÉTODO
    if request.method != 'POST':
        return None
    try:
        json_peticion = json.loads(request.body)
        usuario = Usuarios()
        usuario.nombre = json_peticion['name']
        usuario.email = json_peticion['email']
        usuario.contrasena = json_peticion['password']
	#COMPRUEBA QUE NO FALTA NINGÚN PARÁMETRO NECESARIO
        if usuario.nombre == '' or usuario.email == '' or usuario.contrasena == '':
            return JsonResponse({"status": "Faltan parámetros"}, status=400)
        else:
		#COMPRUEBA QUE EL NOMBRE DE USUARIO NO COINCIDE CON NINGUNO DE LA BASE DE DATOS
            if Usuarios.objects.filter(nombre=usuario.nombre).exists():
                return JsonResponse({"status": "Nombre de usuario ya existente"}, status=409)
            else:
			#COMPRUEBA QUE EL MAIL NO COINCIDE CON NINGUNO DE LA BASE DE DATOS
                if Usuarios.objects.filter(email=usuario.email).exists():
                    return JsonResponse({"status": "Email ya existente"}, status=409)
                    print("hola")
                else:
			#SI TODO LO ANTERIOR NO OCURRE, SE REGISTRA CORRECTAMENTE
                    usuario.set_password(json_peticion['password'])
                    payload = {
                        'nombre': usuario.nombre,
                        'email': usuario.email
                    }
                   #TOKENS PARA CONTRASEÑA
                    secret = 'messifiltrado'
                    token = jwt.encode(payload, secret, algorithm='HS256')
                    usuario.tokensession = token
                    usuario.save()
                    return JsonResponse({"status": "Bien."}, status=201)
    except (JSONDecodeError, Exception):
        return JsonResponse({"status": "Error"})


#BET--GET QUE OBTIENE LOS DATOS EDITABLES DENTRO DE UN USER
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
def datos_user(request, id_solicitado):
	datos = Usuarios.objects.get(id = id_solicitado) 
	resultado = {
		'Nombre': datos.nombre,
		'NombreUser': datos.nombreuser
	}
	return JsonResponse(resultado, json_dumps_params={'ensure_ascii':False});

#OMAR--GET OBTIENE LOS SEGUIDORES DE UN USUARIO
def seguidores(request, id_solicitado):
	datos = Follow.objects.get(idseguido = id_solicitado)
	tokenRecibido = request.headers.get('Auth-Token')
	datos.idseguido = Usuarios.objects.get(tokensession = tokenRecibido)
	resultado = {
		'idSeguidor': count(datos.idseguidor)
	}
	return JsonResponse(resultado, json_dumps_params={'ensure_ascii': False})

#OMAR--GET QUE OBTIENE LOS SEGUIDOS
def seguidos(request, id_solicitado):
	usuario = Usuarios.objects.get(id = id_solicitado)
	datos = Follow.objects.get(idseguido = usuario.id)
	tokenRecibido = request.headers.get('Auth-Token')
	datos.idseguido = Usuarios.objects.get(tokensession = tokenRecibido)
	resultado = {
		'idSeguidor':count( datos.idseguido)
	}
	return JsonResponse(resultado, json_dumps_params={'ensure_ascii': False})

#BET--POST PARA LAS SESIONES.
@csrf_exempt
def sessions(r):
    # Si el método es POST, se intenta crear una nueva sesión
    if r.method == "POST":

        # Se intenta obtener el cuerpo de la petición
        try:
            data = json.loads(r.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "Bad request"}, status=400)

        # Se intenta obtener el usuario de la BBDD con los datos obtenidos
        try:
            user = Users.objects.get(email=data["email"])
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Not found"}, status=404)

        # Se intenta verificar la contraseña
        if user.check_password(data["password"]):
            # Se genera el token
            token_string = get_random_string(length=32)
            new_token = Tokens()
            new_token.token = token_string
            new_token.userid = user
            new_token.save()

            # Se devuelve un 201
            return JsonResponse(
                {"sessionToken": token_string},
                json_dumps_params={"ensure_ascii": False},
                status=201,
            )
        else:
            # Se devuelve 401
            return JsonResponse({"message": "Unauthorized"}, status=401)
