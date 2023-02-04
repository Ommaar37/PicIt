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

INSERT INTO Usuarios (id, NombreUser, Nombre, Apellidos, Biografia, Pais, Genero, Email, Contrasena, TokenSession) VALUES 
("1", "Juan123", "Juan", "", "", "", "", "juan.perez@ejemplo.com", "JuanPerez123", "abc123"),
("2", "Maria123", "Maria", "Gomez", "Hola me llamo María y me gusta la fotografía", "Australia", "Femenino", "maria.gomez@ejemplo.com", "MariaGomez123", "def456");

INSERT INTO Mensaje (id, fecha, mensaje, idUser) VALUES 
("1", "", "Hola", "1"),
("2", "", "Holaa, q tal?", "2"),
("3", "", "Muy bien, y tu?", "1"),
("4", "", "Genial, oye hace mucho que no nos vemos, te apetece ir a tomar un café por la tarde?", "2"),
("5", "", "Hoy imposible", "1"),
("6", "", "Pero mañana estoy libre, puedes?", "1"),
("7", "", "Siii claro", "2"),
("8", "", "Sin problema", "2"),
("9", "", "A las 17:00?", "2"),
("10", "", "Perfecto", "1");

INSERT INTO Follow (idFollow, idSeguidor, idSeguido) VALUES 
("1", "1", "2"),
("2", "2", "1");

INSERT INTO Carpetas (id, Nombre, idUser) VALUES 
("1", "Hogar", "1"),
("2", "Verano", "1"),
("3", "Viajes", "2");

INSERT INTO Publicaciones (id, Titulo, Fecha, Descripcion, Imagen, idUser) VALUES 
("1", "Conejo", curdate(), "Conejo tomando el sol antes de surfear", "conejo.png", "1"),
("2", "Coche", curdate(), "Coche de carreras", "coche.png", "1"),
("3", "Tatuajes brazo", curdate(), "manga entera de tatuajes en el brazo", "tatuaje.png", "1"),
("4", "Paisaje natural", curdate(), "Atardecer en el campo", "paisaje.png", "1"),
("5", "Comida desayuno", curdate(), "Tortitas con sirope de chocolate", "comida.png", "1"),
("6", "Concierto de verano", curdate(), "Concierto de un festival", "concierto.png", "2"),
("7", "Personaje de anime", curdate(), "Mikasa en Attack On Taitan", "anime.png", "2"),
("8", "Carrera", curdate(), "Carrera de atletismo", "deportes.png", "2"),
("9", "Outfit boda", curdate(), "Conjunto para invitado de boda", "ropa.png", "2"),
("10", "Cuchara", curdate(), "Dibujo de una cuchara", "dibujo.png", "2"),
("11", "Florencia", curdate(), "Catedral de Santa Maria del Fiore", "arquitectura.png", "2"),
("12", "Salón", curdate(), "Decoración de salón en tonos claros", "decoracion.png", "2"),
("13", "Superman", curdate(), "Una frase de Superman", "frase.png", "2"),
("14", "Animales de papel", curdate(), "Animales cuadrados hechos doblando papel", "manualidad.png", "2");

INSERT INTO Tags (id, Nombre) VALUES 
("1", "Animales"),
("2", "Anime"),
("3", "Arquitectura"),
("4", "Arte"),
("5", "Coches"),
("6", "Comida"),
("7", "Decoración hogar"),
("8", "Deportes"),
("9", "Dibujos"),
("10", "Frases"),
("11", "Libros"),
("12", "Manualidades"),
("13", "Música"),
("14", "Naturaleza"),
("15", "Paisajes"),
("16", "Ropa"),
("17", "Tatuajes");

INSERT INTO Likes (id, idUser, idPublic) VALUES 
("1", "1", "1"),
("2", "1", "2"),
("3", "1", "3"),
("4", "1", "4"),
("5", "1", "5"),
("6", "2", "6"),
("7", "2", "7"),
("8", "2", "8"),
("9", "2", "9"),
("10", "2", "10");

INSERT INTO Public_carpetas (idPublic_carpeta, idPublic, idCarpeta) VALUES 
("1", "1", "1"),
("2", "2", "1"),
("3", "3", "2"),
("4", "4", "2"),
("5", "5", "2"),
("6", "6", "3"),
("7", "7", "3"),
("8", "8", "3"),
("9", "9", "3"),
("10", "10", "3");

INSERT INTO AsignarTags (idAsignacion, idTag, idPublic) VALUES 
("1", "1", "1"),
("2", "14", "1"),
("3", "15", "1"),
("4", "5", "2"),
("5", "8", "2"),
("6", "4", "3"),
("7", "9", "3"),
("8", "17", "3"),
("9", "14", "4"),
("10", "15", "4"),
("11", "6", "5"),
("12", "13", "6"),
("13", "2", "7"),
("14", "4", "7"),
("15", "9", "7"),
("16", "8", "8"),
("17", "16", "9"),
("18", "9", "10"),
("19", "3", "11"),
("20", "4", "11"),
("21", "15", "11"),
("22", "3", "12"),
("23", "7", "12"),
("24", "10", "13"),
("25", "11", "13"),
("26", "12", "14");
