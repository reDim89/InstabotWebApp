from app.views import index, login, mybot, show_log


def setup_routes(app):
    '''
    Setting up routes for GET/POST methods on main page and bot page.
    Adding css tyles to app.
    '''
    app.router.add_get('/', index)
    app.router.add_post('/', login)
    app.router.add_get('/mybot', mybot)
    app.router.add_post('/mybot', show_log)
    app.router.add_static('/static',
                          path=str('static'),
                          name='static')
