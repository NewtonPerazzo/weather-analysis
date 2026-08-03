from fastapi import FastAPI
from app.router.open_meteo_router import open_meteo_router

app = FastAPI(
    title="Weather Analysis API",
    version="1.0.0" 
)
@app.get('/health')
def health_check():
    return {"status": "ok"}

app.include_router(open_meteo_router)
