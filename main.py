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
    "esrb_rating",
    "parent_platforms",
    "genres",
]

# Elimino las columnas que no están en la lista (Columnas_DF)
games_df = games_df.drop(columns=games_df.columns.difference(Columnas_Df))

# Extrae los diccionarios en nuevos DFs, para guardar en RDS

platforms_df = extract(games_df, 'platforms','platform')
store_df= extract(games_df, 'stores','store')
parent_platforms_df=extract(games_df, 'parent_platforms','platform')










# # Convierto las siguientes columnas a un formato JSON, para alojar en la BD RDS.

# games_df['slug'] = games_df['slug'].apply(lambda x: json.dumps(x))
# games_df['platforms'] = games_df['platforms'].apply(lambda x: json.dumps(x))
# games_df['stores'] = games_df['stores'].apply(lambda x: json.dumps(x))
# games_df['esrb_rating'] = games_df['esrb_rating'].apply(lambda x: json.dumps(x))
# games_df['esrb_rating'] = games_df['esrb_rating'].apply(lambda x: json.dumps(x))
# games_df['parent_platforms'] = games_df['parent_platforms'].apply(lambda x: json.dumps(x))
# games_df['genres'] = games_df['genres'].apply(lambda x: json.dumps(x))

# # CARGA DE DATOS       

# #Guardo en la variabla el Schema de coderhouse

# schema= "martindattoliv_coderhouse"

# RDSconn.execute(
#     f"""
#     CREATE EXTENSION IF NOT EXISTS "jsonb";
#     """
# )

# # Creo la Tabla en la BD
# RDSconn.execute(
#     f"""
#         DROP TABLE IF EXISTS {schema}.games;
#         CREATE TABLE {schema}.games(
#         id INT,
#         slug JSONB,
#         name VARCHAR (256),
#         playtime INT,
#         platforms JSONB,
#         stores JSONB,
#         released TIMESTAMP,
#         rating FLOAT,
#         rating_top INT,
#         updates TIMESTAMP,
#         esrb_rating JSONB,
#         parent_platforms JSONB,
#         genres JSONB
#         );
#     """
# )

# games_df.to_sql(
#     name="games",
#     con=RDSengine,
#     schema=schema,
#     if_exists="replace",
#     index=False
    
# )
