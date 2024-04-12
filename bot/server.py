import uvicorn
import os
from fastapi import FastAPI
from http_routes import threads


app = FastAPI()
app.include_router(threads.router, prefix='/api')


if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    uvicorn.run('server:app', host="0.0.0.0", port=8080, workers=1, reload=True, app_dir='.')