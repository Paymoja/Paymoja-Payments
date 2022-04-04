import uvicorn as uvicorn
import json
import os
from pathlib import Path
from starlette.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi_caching import CacheManager, InMemoryBackend

from models import payments_model
from routers import payments_controller
from utils.database import engine
import fastapi_chameleon
import structlog
from fastapi.templating import Jinja2Templates

struct_logger = structlog.get_logger(__name__)

app = FastAPI(debug=True)
dev_mode = True

folder = os.path.dirname(__file__)
template_folder = os.path.join(folder, 'static/templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

fastapi_chameleon.global_init(template_folder, auto_reload=dev_mode)
BASE_PATH = Path(__file__).resolve().parent

jinja_templates = Jinja2Templates(directory=str(BASE_PATH/"static/templates"))


cache_backend = InMemoryBackend()
cache_manager = CacheManager(cache_backend)


def configure():
    configure_settings()
    configure_routes()
    configure_database()


def configure_routes():
    app.include_router(payments_controller.router)


def configure_settings():
    file = Path('settings.json').absolute()
    if not file.exists():
        struct_logger.error(event="configure_settings", error="settings file has not been found")
        raise Exception("settings file has not been file. Service can not continue, please see settings template")

    with open('settings.json') as fin:
        return json.load(fin)


def configure_database():
    payments_model.Base.metadata.create_all(bind=engine)

@app.get("/")
@fastapi_chameleon.template('home/index.pt')
async def root():
    return {'service': 'Paymoja', 'version': '1.0'}


if __name__ == '__main__':
    configure()
    uvicorn.run(app, port=8081, host="0.0.0.0")
else:
    configure()
