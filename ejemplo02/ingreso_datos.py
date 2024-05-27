from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# se importa la clase(s) del 
# archivo genera_tablas
from genera_tablas import Club, Jugador

# se importa información del archivo configuracion
from configuracion import cadena_base_datos
# se genera enlace al gestor de base de
# datos
# para el ejemplo se usa la base de datos
# sqlite
engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()


with open('data/datos_clubs.txt', 'r', encoding='utf-8') as f:
    for line in f:
        nombre, deporte, fundacion = line.strip().split(';')
        club = Club(nombre=nombre, deporte=deporte, fundacion=int(fundacion))
        session.add(club)

session.commit()
	
with open('data/datos_jugadores.txt', 'r', encoding='utf-8') as archivo2:
    # obtener las líneas del archivo
    data2 = archivo2.readlines()

# Se crean objetos de tipo Jugador
for lineas2 in data2:
    clubJuga, posicionJuga, dorsalJuga, nombreJuga = lineas2.strip().split(';')
    # Buscar el club correspondiente en la base de datos
    club = session.query(Club).filter_by(nombre=clubJuga).one()
    jugador = Jugador(nombre=nombreJuga, dorsal=int(dorsalJuga), posicion=posicionJuga, club=club)
    session.add(jugador)
    
session.commit()