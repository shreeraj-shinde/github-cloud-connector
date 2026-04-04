import uvicorn
from app.config import get_settings

#  Load the ENV varaibles
settings = get_settings()

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=settings.PORT, reload=True)