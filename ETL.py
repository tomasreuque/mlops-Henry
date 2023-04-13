import pandas as pd
import os

# Directorio de los archivos csv
directory = (r"C:\Users\tomas\Desktop\mlops-Henry\csv")
dataframes = []

# Bucle a través del directorio para leer los archivos csv
for filename in os.listdir(directory):
    if filename.endswith(".csv"): # Lee solo los csv
        # Agrego la columna plataforma aprovechando el loop
        df = pd.read_csv(os.path.join(directory, filename))
        df["plataforma"] = filename.split("_")[0]  # Extraigo el nombre de la plataforma 
        
        # Mergeo la primera letra de archivo con la columna show_id para 
        df["id"] = filename.split("_")[0][0] + df["show_id"].astype(str)
        
        # Append the dataframe to the list
        dataframes.append(df)

# Concatenación de dataframes
merged_df = pd.concat(dataframes)

# Extraigo los valores duration en columna rating
duration_regex = r'(\d+\s(min|seasons)|\d+\s\w+\s\d+\s\w+)?'  # Expresión regular para hallar valores de duración
merged_df['duration_extracted'] = merged_df['rating'].str.extract(duration_regex)[0]

# Ingerto los NaN con los valores extraídos
merged_df['duration'].fillna(value=merged_df['duration_extracted'], inplace=True)

# Dropeo la columna duration_extracted
merged_df.drop('duration_extracted', axis=1, inplace=True)

# Rellenamos los NaN values con la letra G
merged_df["rating"].fillna('G', inplace=True)

# Transformando fechas
merged_df['date_added'] = pd.to_datetime(merged_df['date_added'], infer_datetime_format=True, errors='coerce')

# Divido la columna "duration" en duration_int y duration_type. 
merged_df[['duration_int', 'duration_type']] = merged_df['duration'].str.extract('(\d+)\s*(\w+)')

# Reemplazo "seasons" por "season":
merged_df["duration_type"] = merged_df["duration_type"].str.replace("seasons", "season")

# Transformo en minúsculas las entradas string 
merged_df = merged_df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

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
merged_df = merged_df.merge(df_mean[['movieId', 'mean_rating']], how='left', left_on='id', right_on='movieId')
# Guardamos el archivo final
merged_df.to_csv("streamingfinal.csv", index=False)