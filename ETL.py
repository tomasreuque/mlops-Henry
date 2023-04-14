import pandas as pd
import os

# Directorio de los archivos csv
directory = (r"C:\Users\tomas\Desktop\mlops-Henry\csv")
raw = []

# Bucle a través del directorio para leer los archivos csv
for filename in os.listdir(directory):
    if filename.endswith(".csv"): # Lee solo los csv
        # Agrego la columna plataforma aprovechando el loop
        df = pd.read_csv(os.path.join(directory, filename))
        df["plataforma"] = filename.split("_")[0]  # Extraigo el nombre de la plataforma
        # Append the dataframe to the list
        raw.append(df)

# Concatenación de dataframes
peliculas = pd.concat(raw)
##hago un drop
peliculas.drop(['id', 'duration_int', 'duration_type'], axis=1, inplace=True)
#creo variable id en base a la columna plataforma
peliculas["id"] = peliculas["plataforma"].apply(lambda x: x.split("_")[0][0]) + peliculas["show_id"]
# Extraigo los valores duration en columna rating
duration_regex = r'(\d+\s(min|seasons)|\d+\s\w+\s\d+\s\w+)?'  # Expresión regular para hallar valores de duración
peliculas['duration_extracted'] = peliculas['rating'].str.extract(duration_regex)[0]

# Ingerto los NaN con los valores extraídos
peliculas['duration'].fillna(value=peliculas['duration_extracted'], inplace=True)

# Dropeo la columna duration_extracted
peliculas.drop('duration_extracted', axis=1, inplace=True)

# Rellenamos los NaN values con la letra G
peliculas["rating"].fillna('G', inplace=True)

# Transformando fechas
peliculas['date_added'] = pd.to_datetime(peliculas['date_added'], infer_datetime_format=True, errors='coerce')

# Divido la columna "duration" en duration_int y duration_type. 
peliculas[['duration_int', 'duration_type']] = peliculas['duration'].str.extract('(\d+)\s*(\w+)')

# Reemplazo "seasons" por "season":
peliculas["duration_type"] = peliculas["duration_type"].str.replace("seasons", "season")

# Transformo en minúsculas las entradas string 
peliculas = peliculas.applymap(lambda x: x.lower() if isinstance(x, str) else x)

# Obtengo el promedio de ratings de todos los movieIds
dir_path = r"C:\Users\tomas\Desktop\mlops-Henry\ratings" # Se establece el directorio donde se encuentran los archivos CSV con los ratings
csv_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.csv')] # Se crea una lista con los nombres de todos los archivos CSV en el directorio

df_concat = pd.DataFrame() # Se crea un dataframe vacío para alojar los nuevos

# Concateno los archivos csv
for file in csv_files:
    df = pd.read_csv(file)
    df_concat = pd.concat([df_concat, df], ignore_index=True)

# Computo el promedio de movieIds
df_mean = df_concat.groupby('movieId', as_index=False).mean().rename(columns={'rating': 'mean_rating'})

# Hago un merge de a columna
peliculas = peliculas.merge(df_mean[['movieId', 'mean_rating']], how='left', left_on='id', right_on='movieId', suffixes=('', '_mean'))
peliculas = peliculas.loc[:, ~peliculas.columns.str.endswith(('_x', '_y'))]

##hago un drop
peliculas.drop(['show_id', 'movieId'], axis=1, inplace=True)

# Guardamos el archivo final
peliculas.to_csv("streamingfinal.csv", index=False)