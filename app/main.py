import aiohttp_jinja2
import jinja2

from aiohttp import web
from app.routes import setup_routes


app = web.Application()
app['bot'] = None
app['thread'] = None
app['message'] = ''

aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader('templates'))
setup_routes(app)
web.run_app(app, port=8888)
