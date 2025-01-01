from fastapi import FastAPI
from routes.api import router as api_router

app = FastAPI()

# Include the router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the LLM Testing API"}
