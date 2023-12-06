# Del Script de Conexiones, me traigo las variables con las que voy a Trabajar.
from utils import *
import requests
import json


# Extraigo datos de la api, convirtiendo en un JSON, para luego utilizar en DF
response = requests.get(api_url)
data = response.json()
games_df = pd.DataFrame(data["results"])

# Selecciono las columnas que me van a servir del DF obtenido
Columnas_Df = [
    "id",
    "slug",
    "name",
    "playtime",
    "platforms",
    "stores",
    "released",
    "rating",
    "rating_top",
    "updated",
    "parent_platforms",
    "genres",
]

# Elimino las columnas que no están en la lista (Columnas_DF)
games_df = games_df.drop(columns=games_df.columns.difference(Columnas_Df))

# Extrae los campos que contienen los diccionarios con clave en nuevos DFs, para almacenar en RDS

platforms_df = extraer_dicc(games_df, "platforms", "platform")
store_df = extraer_dicc(games_df, "stores", "store")
parent_platforms_df = extraer_dicc(games_df, "parent_platforms", "platform")

# Extrae los campos que contienen los diccionarios sin clave en nuevos DFs, para almacenar en RDS
genres_df = pd.DataFrame(games_df["genres"].explode().tolist())
genres_df.drop_duplicates().set_index("id")

# Genera una lista de los valores unicos ('id') de las siguiente columnas, para luego realizar un explode y asi relacionar con los DF almacenados.

games_df["platform_ids"] = games_df["platforms"].apply(
    lambda x: extraer_id(x, "platform")
)
games_df["store_ids"] = games_df["stores"].apply(lambda x: extraer_id(x, "store"))
games_df["parent_platform_ids"] = games_df["parent_platforms"].apply(
    lambda x: extraer_id(x, "platform")
)
games_df["genre_ids"] = games_df["genres"].apply(lambda x: [genre["id"] for genre in x])

# Dropeo las columnas ya convertidas.

col_drop = ["platforms", "stores", "parent_platforms", "genres"]
games_df = games_df.drop(columns=col_drop)


# CARGA DE DATOS

# Guardo en la variabla el Schema de coderhouse

schema = "martindattoliv_coderhouse"

# Creo la Tabla en la BD
RDSconn.execute(
    f"""
        DROP TABLE IF EXISTS {schema}.games;
        CREATE TABLE {schema}.games(
        id INT PRIMARY KEY,
        slug VARCHAR(255),
        name VARCHAR(255),
        playtime INT,
        released DATE,
        rating FLOAT,
        rating_top INT,
        updated TIMESTAMP,
        platform_ids INTEGER[],
        store_ids INTEGER[],
        parent_platform_ids INTEGER[],
        genre_ids INTEGER[]     
    );
"""
)


games_df.to_sql(
    name="games", con=RDSengine, schema=schema, if_exists="append", index=False
)

