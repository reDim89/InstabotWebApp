#!venv/bin/python
# -*- coding: utf-8 -*-
import os
import aiohttp_jinja2
import aiohttp


from app.src.instabot import InstaBot
from app.src.stoppable_thread import StoppableThread

from threading import Thread


async def index(request):
    '''
    Render main page template and status message (if exists).
    '''
    await request
    message = request.app['message']

    context = {'title': 'Main', 'message': message}
    return aiohttp_jinja2.render_template('index.html', request, context)


async def login(request):
    '''
    Collect data from login form, log in and run bot instance in daemon thread.
    See https://docs.python.org/3/library/threading.html#thread-objects
    '''
    data = await request.post()

    login = data['login']
    password = data['password']
    like_per_day = int(data['like_per_day'])
    comments_per_day = int(data['comments_per_day'])
    follow_per_day = int(data['follow_per_day'])

    bot = InstaBot(login=login,
                   password=password,
                   like_per_day=like_per_day,
                   comments_per_day=comments_per_day,
                   follow_per_day=follow_per_day,
                   log_mod=2)

    # Start separate thread able to receive stop event

    t = StoppableThread(target=runBot, args=(bot, ))
    t.setDaemon(True)
    t.start()

    # Store pointers to thread and bot in app instance

    request.app['thread'] = t
    request.app['bot'] = bot

    return aiohttp.web.HTTPFound('/mybot')


async def mybot(request):
    '''
    Render bot page template.
    '''

    await request
    context = {'title': 'Bot control panel'}
    return aiohttp_jinja2.render_template('mybot.html', request, context)


async def show_log(request):
    '''
    Receive data from submit buttons and either stop bot or show it's log.
    '''

    data = await request.post()

    # Get bot instance and thread in which it's running

    t = request.app['thread']
    bot = request.app['bot']

    # Check data from submit button

    if bot and 'refresh' in data.keys():

        # Fetch log data from bot instance and re-render page

        context = {'title': 'Bot control panel', 'log': bot.log_full_text}
        return aiohttp_jinja2.render_template('mybot.html', request, context)

    elif bot and 'logout' in data.keys():

        # Send stop event and go to main page

        t.stop()
        request.app['message'] = 'Bot is stopped'
        return aiohttp.web.HTTPFound('/')

    else:

        # Other cases handling

        request.app['message'] = 'Your are not authorized'
        return aiohttp.web.HTTPFound('/')


def runBot(bot):
    '''
    Function to run bot in auto-mod
    '''
    bot.new_auto_mod()
