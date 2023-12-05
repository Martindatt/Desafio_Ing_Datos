from configparser import ConfigParser
import sqlalchemy as sa
import requests
import pandas as pd


"SERVIDOR REDSHIFT"
# Crear una conexion a la Base de datos a partir de un archivo de Configuracion.
def String_connect(config_path, config_section):
    # Leer archivo de configuracion
    parser = ConfigParser()
    parser.read(config_path)

    # Lee la Seccion de Configuracion Redshift

    config = parser[config_section]
    host = config["host"]
    user = config["user"]
    port = config["port"]
    dbname = config["dbname"]
    pwd = config["pass"]

    # Construye la Cadena de Conexion
    conn_string = f"postgresql://{user}:{pwd}@{host}:{port}/{dbname}"

    return conn_string


# Crear conexion a la Base de Datos.
def Connect_db(conn_string):
    engine = sa.create_engine(conn_string)
    conn = engine.connect()
    return conn, engine


"CONEXION API"
# Crear Conexion a la API
def Stringapi_connect(config_path, config_section):
    parser = ConfigParser()
    parser.read(config_path)

    config = parser[config_section]
    Key = config["Clientkey"]
    FechaIni = config["Fecha_Ini"]
    FechaFin = config["Fecha_Fin"]
    # Construye la Cadena de Conexion
    connapi_string = (
        f"https://api.rawg.io/api/games?dates={FechaIni},{FechaFin}&key={Key}"
    )
    # Retorna URL
    return connapi_string


# Genero una funcion para observar el estado de la api.
def get_api_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Lanzará una excepción si el código de estado HTTP no es 200

        data = response.json()
        return data

    except requests.exceptions.HTTPError as errh:
        raise RuntimeError(f"Error HTTP: {errh}")

    except requests.exceptions.ConnectionError as errc:
        raise RuntimeError(f"Error de Conexión: {errc}")

    except requests.exceptions.Timeout as errt:
        raise RuntimeError(f"Tiempo de espera agotado: {errt}")

    except requests.exceptions.RequestException as err:
        raise RuntimeError(f"Error en la solicitud: {err}")


"CONEXIONES"

"REDSHIFT"
# Conectar a la Base de Datos
config_dir = "config/config.ini"
String_connect = String_connect(config_dir, "redshift")
try:
    RDSconn, RDSengine = Connect_db(String_connect)

except Exception as e:
    # Si hay un error, imprime el mensaje de error
    raise Exception(f"Error durante la conexión a la base de datos: {str(e)}")

"API"

# Conectar con la API de Juegos (RAWG)
config_dir = "config/config.ini"
api_url = Stringapi_connect(config_dir, "api_juegos")
# Observamos si ingreso a la API
try:
    api_data = get_api_data(api_url)

except RuntimeError as e:
    raise RuntimeError(f"Error en la conexión a la API: {e}")



"EXTRAER DICCIONARIOS CON CLAVE"

def extract (df, column,key):

    # Lista para almacenar los diccionarios
    platforms_data = []

    # Iterar sobre las filas del DataFrame
    for _, row in df.iterrows():
        # Información de la columna especificada
        platforms_info = row[column]

        # Iterar sobre los diccionarios dentro de la lista (extraer y agregar a la lista)
        for platform_dict in platforms_info:
            platform_info = platform_dict[key]
            platforms_data.append(platform_info)

    # Crear un nuevo DataFrame llamado 
    result_df = pd.DataFrame(platforms_data).drop_duplicates().set_index('id')

    return result_df



