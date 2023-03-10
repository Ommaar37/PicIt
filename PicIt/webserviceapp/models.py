# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.hashers import make_password

class Carpetas(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    iduser = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='idUser')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Carpetas'


class Follow(models.Model):
    idfollow = models.AutoField(db_column='idFollow', primary_key=True)  # Field name made lowercase.
    idseguidor = models.ForeignKey('Usuarios', related_name='seguidor_set',on_delete=models.CASCADE)  # Field name made lowercase.
    idseguido = models.ForeignKey('Usuarios', related_name='seguido_set', on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Follow'


class Likes(models.Model):
    iduser = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='idUser')  # Field name made lowercase.
    idpublic = models.ForeignKey('Publicaciones', models.DO_NOTHING, db_column='idPublic')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Likes'

class PublicCarpetas(models.Model):
    idpublic_carpeta = models.AutoField(db_column='idPublic_carpeta', primary_key=True)  # Field name made lowercase.
    idpublic = models.ForeignKey('Publicaciones', models.DO_NOTHING, db_column='idPublic')  # Field name made lowercase.
    idcarpeta = models.ForeignKey(Carpetas, models.DO_NOTHING, db_column='idCarpeta')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Public_carpetas'


class Publicaciones(models.Model):
    titulo = models.CharField(db_column='Titulo', max_length=50)  # Field name made lowercase.
    fecha = models.DateField(db_column='Fecha')  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=500)  # Field name made lowercase.
    imagen = models.CharField(db_column='Imagen', max_length=10000)  # Field name made lowercase.
    iduser = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='idUser')  # Field name made lowercase.
    idtag = models.ForeignKey('Tags', models.DO_NOTHING, db_column='idTag')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Publicaciones'


class Tags(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tags'


class Usuarios(models.Model):
    nombreuser = models.CharField(db_column='NombreUser', max_length=50)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    apellidos = models.CharField(db_column='Apellidos', max_length=100, blank=True, null=True)  # Field name made lowercase.
    biografia = models.CharField(db_column='Biografia', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    genero = models.CharField(db_column='Genero', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100)  # Field name made lowercase.
    contrasena = models.CharField(db_column='Contrasena', max_length=256)  # Field name made lowercase.
    tokensession = models.CharField(db_column='TokenSession', max_length=300)  # Field name made lowercase.
    def set_password(self, raw_password):
        self.contrasena = make_password(raw_password)
    class Meta:
        managed = False
        db_table = 'Usuarios'

class Mensaje(models.Model):
    fecha = models.DateField()
    mensaje = models.CharField(max_length=300)
    iduser = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='idUser')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mensaje'
