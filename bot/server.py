import uvicorn
import logging
from fastapi import FastAPI

from baski.env import get_env
from http_routes import threads


app = FastAPI()
app.include_router(threads.router, prefix='/api')


if __name__ == '__main__':
    logging.root.setLevel(logging.DEBUG if get_env('DEBUG', False) else logging.INFO)
    port = int(get_env("PORT", 8080))
    uvicorn.run('server:app', host="0.0.0.0", port=8080, reload=get_env('DEBUG', False))