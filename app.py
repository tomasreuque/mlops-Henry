import pandas as pd
from fastapi import FastAPI

# Cargar el archivo CSV con la información de las películas
peliculas = pd.read_csv(r"streamingfinal.csv")

# Inicializar la aplicación FastAPI
app = FastAPI()

# Endpoint de bienvenida
@app.get("/")
async def welcome():
    return {"message": "Bienvenido a mi API"}

# Endpoint para obtener la película con mayor duración segun año, plataforma 
@app.get("/get_max_duration/{year}/{platform}/{duration_type}")
async def get_max_duration(year: int, platform: str, duration_type: str):
    filtered_df = peliculas[(peliculas['type'] == 'movie') & 
                     (peliculas['release_year'] == year) & 
                     (peliculas['plataforma'] == platform) & 
                     (peliculas['duration_type'] == duration_type)]
    sorted_df = filtered_df.sort_values(by='duration_int', ascending=False)
    max_duration_movie = sorted_df.iloc[0][['title', 'duration']]
    return max_duration_movie.to_dict()

# Endpoint para obtener pelicula con mejor puntuacion que que score
@app.get("/score_count/{year}/{platform}/{scored}")
def score_count(platform: str, scored: float, year: int):
    # Filtrar los datos según los criterios especificados
    filtered_df = peliculas[(peliculas['plataforma'] == platform) & 
                     (peliculas['mean_rating'] > scored) & 
                     (peliculas['release_year'] == year) & 
                     (peliculas['type'] == 'movie')]
    count = len(filtered_df)
    return count

# Endpoint para retornar la cantidad solo de peliculas de una plataforma solo de las que tenemos
@app.get("/get_count_platform/{platform}")
def get_count_platform(platform: str):
    # Valida que la plataforma sea una de las cuatro permitidas
    valid_platforms = ['amazon', 'netflix', 'hulu', 'disney']
    if platform not in valid_platforms:
        return {"error": "La plataforma no es válida"}
    
    # Filtra el dataframe para contar las películas
    filtered_df = peliculas[(peliculas["type"] == "movie") & 
                           (peliculas['plataforma'] == platform)]
    count = len(filtered_df)
    
    return count

# Endpoint para obtener el actor que más se repite según plataforma y año
@app.get("/get_actor")
def get_actor(platform: str, year: int):
    # Filtrar los datos según los criterios especificados
    filtered_df = peliculas[(peliculas['plataforma'] == platform) & 
                     (peliculas['release_year'] == year)]
    actor_counts = filtered_df['cast'].str.split(', ', expand=True).stack().value_counts()
    max_actor_count = actor_counts.max()
    max_actor = actor_counts[actor_counts == max_actor_count].index[0]
    return max_actor

# Endpoint para obtener la cantidad de contenidos/productos por país y año
@app.get("/prod_per_county")
def prod_per_county(tipo: str, pais: str, anio: int):
    # Filtrar los datos según los criterios especificados
    filtered_df = peliculas[(peliculas['country'] == pais) & 
                     (peliculas['release_year'] == anio) & 
                     (peliculas['type'] == tipo)]
    count = len(filtered_df)

# Endpoint 
@app.get("/get_contents/{rating}")
async def get_contents(rating: str):
    filtered_df = peliculas[peliculas['rating'] == rating]
    count = len(filtered_df)
    return {"count": count}
