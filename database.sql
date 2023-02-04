USE PicIt;

CREATE TABLE Usuarios(
    id int not null auto_increment primary key,
    NombreUser varchar(50) not null,
    Nombre varchar(50) not null,
    Apellidos varchar(100) null,
    Biografia varchar(2000) null,
    Pais varchar(50) null,
    Genero varchar(20) null
    Email varchar(100) not null,
    Contrasena varchar(30) not null,
    TokenSession varchar(100) not null,
);

CREATE TABLE Mensaje(
    id int primary key auto_increment not null,
    fecha date not null,
    mensaje varchar(300) not null,
    idUser int not null
);


CREATE TABLE Follow(
    idFollow int primary key auto_increment not null,
    idSeguidor int not null,
    idSeguido int not null
);


CREATE TABLE Carpetas(
    id int primary key auto_increment not null,
    Nombre varchar(50) not null,
    idUser int not null
);

CREATE TABLE Publicaciones(
    id int primary key auto_increment not null,
    Titulo varchar(50) not null,
    Fecha date not null,
    Descripcion varchar(500) not null,
    Imagen  varchar(10000) not null,
    idUser int not null
);

CREATE TABLE Tags(
    id int primary key auto_increment not null,
    Nombre varchar(50) not null
);

CREATE TABLE Likes(
    id int primary key auto_increment not null,
    idUser int not null,
    idPublic int not null
);

CREATE TABLE Public_carpetas(
    idPublic_carpeta int not null auto_increment primary key,
    idPublic int not null,
    idCarpeta int not null
);

CREATE TABLE AsignarTags(
    idAsignacion int not null auto_increment primary key,
    idTag int not null,
    idPublic int not null
);

ALTER TABLE Mensaje ADD CONSTRAINT FOREIGN KEY (idUser) REFERENCES Usuarios(id);

ALTER TABLE Follow ADD CONSTRAINT FOREIGN KEY (idSeguidor) REFERENCES Usuarios(id);
ALTER TABLE Follow ADD CONSTRAINT FOREIGN KEY (idSeguido) REFERENCES Usuarios(id);

ALTER TABLE Carpetas ADD CONSTRAINT FOREIGN KEY (idUser) REFERENCES Usuarios(id);

ALTER TABLE Publicaciones ADD CONSTRAINT FOREIGN KEY (idUser) REFERENCES Usuarios(id);

ALTER TABLE Likes ADD CONSTRAINT FOREIGN KEY (idUser) REFERENCES Usuarios(id);
ALTER TABLE Likes ADD CONSTRAINT FOREIGN KEY (idPublic) REFERENCES Publicaciones(id);

ALTER TABLE Public_carpetas ADD CONSTRAINT FOREIGN KEY (idPublic) REFERENCES Publicaciones(id);
ALTER TABLE Public_carpetas ADD CONSTRAINT FOREIGN KEY (idCarpeta) REFERENCES Carpetas(id);

ALTER TABLE AsignarTags ADD CONSTRAINT FOREIGN KEY (idTag) REFERENCES Tags(id);
ALTER TABLE AsignarTags ADD CONSTRAINT FOREIGN KEY (idPublic) REFERENCES Publicaciones(id);
