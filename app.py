import pandas as pd
from fastapi import FastAPI
from collections import Counter

# importar la base de datos
peliculas = pd.read_csv(r"C:\Users\tomas\Desktop\mlops-Henry\streamingfinal.csv")

# inicializar FastAPI
app = FastAPI()

#bienvenida
@app.get("/")
async def welcome():
    return {"message": "Bienvenido a mi API"}

# endpoint para obtener la película con mayor duración
@app.get("/get_max_duration/{year}/{platform}/{duration_type}")
async def get_max_duration(year: int, platform: str, duration_type: str):
    filtered_df = peliculas[(peliculas['type'] == 'movie') & 
                     (peliculas['release_year'] == year) & 
                     (peliculas['plataforma'] == platform) & 
                     (peliculas['duration_type'] == duration_type)]
    sorted_df = filtered_df.sort_values(by='duration_int', ascending=False)
    max_duration_movie = sorted_df.iloc[0][['title', 'duration']]
    return max_duration_movie.to_dict()

# endpoint para obtener pelicula con mejor puntuacion que que score
@app.get("/score_count/{year}/{platform}/{scored}")
def score_count(platform: str, scored: float, year: int):
    # Filtrar los datos según los criterios especificados
    filtered_df = peliculas[(peliculas['plataforma'] == platform) & 
                     (peliculas['mean_rating'] > scored) & 
                     (peliculas['release_year'] == year) & 
                     (peliculas['type'] == 'movie')]
    count = len(filtered_df)
    return count


# endpoint para retornar la cantidad solo de peliculas de una plataforma solo de las que tenemos
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



import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
