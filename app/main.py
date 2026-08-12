from fastapi import FastAPI
from app.exceptions.exception_handlers import register_exception_handlers
from app.router.analysis_router import analysis_router
from app.router.open_meteo_router import open_meteo_router

app = FastAPI(
    title="Weather Analysis API",
    version="1.0.0" 
)

register_exception_handlers(app)

@app.get('/health')
def health_check():
    return {"status": "ok"}

app.include_router(open_meteo_router)
app.include_router(analysis_router)
