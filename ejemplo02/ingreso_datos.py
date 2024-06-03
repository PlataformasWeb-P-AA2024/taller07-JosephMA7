from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# se importa la clase(s) del archivo genera_tablas
from genera_tablas import Club, Jugador

# se importa información del archivo configuracion
from configuracion import cadena_base_datos
# se genera enlace al gestor de base de datos
# para el ejemplo se usa la base de datos sqlite
engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()

# Lectura y Procesamiento del Archivo datos_clubs.txt
with open('data/datos_clubs.txt', 'r', encoding='utf-8') as f:
    for line in f:
        nombre, deporte, fundacion = line.strip().split(';')
        # se crea una instancia club con estos datos
        club = Club(nombre=nombre, deporte=deporte, fundacion=int(fundacion))
        # se añade la instancia club
        session.add(club)

session.commit()

# Lectura del Archivo datos_jugadores.txt
with open('data/datos_jugadores.txt', 'r', encoding='utf-8') as archivo2:
    # obtener las líneas del archivo
    data2 = archivo2.readlines()

# Creación y Almacenamiento de Objetos Jugador
for lineas2 in data2:
    valores = lineas2.strip().split(';')
    if len(valores) == 4:
        clubJuga, posicionJuga, dorsalJuga, nombreJuga = valores
        # Buscar el club correspondiente en la base de datos
        # Esta línea obtiene el primer resultado encontrado
        club = session.query(Club).filter_by(nombre=clubJuga).one()
        if club is not None:
            try:
                dorsalJuga = int(dorsalJuga)  # Asegurar que el dorsal es un número entero
                jugador = Jugador(nombre=nombreJuga, dorsal=dorsalJuga, posicion=posicionJuga, club=club)
                session.add(jugador)
            except ValueError:
                print(f"Dorsal no es un número: {dorsalJuga} en línea: {lineas2.strip()}")
        else:
            print(f"Club no encontrado: {clubJuga}")
    else:
        print(f"Línea ignorada por formato incorrecto: {lineas2.strip()}")

session.commit()
