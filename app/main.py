import aiohttp_jinja2
import jinja2

from aiohttp import web
from app.routes import setup_routes

# Starting application and initializing variables required for data sharing
# Variables are stored in app instance, for more infomation see:
# http://aiohttp.readthedocs.io/en/stable/web.html?highlight=singleton#data-sharing-aka-no-singletons-please

app = web.Application()
app['bot'] = None
app['thread'] = None
app['message'] = ''

# Loading web page templates
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader('templates'))
setup_routes(app)
