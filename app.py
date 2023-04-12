import pandas as pd
from fastapi import FastAPI

# importar la base de datos
peliculas = pd.read_csv(r"C:\Users\tomas\Desktop\PI_ML_OPS\streamingfinal.csv")

# inicializar FastAPI
app = FastAPI()

#bienvenida
@app.get("/")
async def welcome():
    return {"message": "Bienvenido a mi API"}

# endpoint para obtener la película con mayor duración
@app.get("/get_max_duration")
async def get_max_duration(year: int, platform: str, duration_type: str):
    filtered_df = peliculas[(peliculas['type'] == 'movie') & 
                     (peliculas['release_year'] == year) & 
                     (peliculas['plataforma'] == platform) & 
                     (peliculas['duration_type'] == duration_type)]
    sorted_df = filtered_df.sort_values(by='duration_int', ascending=False)
    max_duration_movie = sorted_df.iloc[0][['title', 'duration']]
    return max_duration_movie.to_dict()

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
