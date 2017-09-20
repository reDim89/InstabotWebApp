#!venv/bin/python
# -*- coding: utf-8 -*-
import os
import aiohttp_jinja2
import aiohttp


from src.instabot import InstaBot
from src.stoppable_thread import StoppableThread

from threading import Thread


def index(request):
    message = request.app['message']
    context = {'title': 'Main', 'message': message}
    return aiohttp_jinja2.render_template('index.html', request, context)


async def login(request):

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
                   follow_per_day=follow_per_day)

    t = StoppableThread(target=runBot, args=(bot, ))
    t.setDaemon(True)
    t.start()

    request.app['thread'] = t
    request.app['bot'] = bot

    return aiohttp.web.HTTPFound('/mybot')


def mybot(request):
    context = {'title': 'Main'}
    return aiohttp_jinja2.render_template('mybot.html', request, context)


async def show_log(request):

    data = await request.post()
    logString = ''

    t = request.app['thread']
    bot = request.app['bot']

    if bot and 'refresh' in data.keys():
        with open(bot.log_full_path, 'r') as log:
            for line in log:
                logString += line

        context = {'log': logString}
        return aiohttp_jinja2.render_template('mybot.html', request, context)
    elif bot and 'logout' in data.keys():
        t.stop()
        request.app['message'] = 'Bot is stopped'
        return aiohttp.web.HTTPFound('/')
    else:
        request.app['message'] = 'Your are not authorized'
        return aiohttp.web.HTTPFound('/')


def runBot(bot):
    bot.new_auto_mod()



'''
async def runBot():

    global bot

        #print("# MODE 0 = ORIGINAL MODE BY LEVPASHA")
        #print("## MODE 1 = MODIFIED MODE BY KEMONG")
        #print("### MODE 2 = ORIGINAL MODE + UNFOLLOW WHO DON'T FOLLOW BACK")
        #print("#### MODE 3 = MODIFIED MODE : UNFOLLOW USERS WHO DON'T FOLLOW YOU BASED ON RECENT FEED")
        #print("##### MODE 4 = MODIFIED MODE : FOLLOW USERS BASED ON RECENT FEED ONLY")
        #print("###### MODE 5 = MODIFIED MODE : JUST UNFOLLOW EVERYBODY, EITHER YOUR FOLLOWER OR NOT")

        ################################
        ##  WARNING   ###
        ################################

        # DON'T USE MODE 5 FOR A LONG PERIOD. YOU RISK YOUR ACCOUNT FROM GETTING BANNED
        ## USE MODE 5 IN BURST MODE, USE IT TO UNFOLLOW PEOPLE AS MANY AS YOU WANT IN SHORT TIME PERIOD

    mode = 0

    #print("You choose mode : %i" %(mode))
    #print("CTRL + C to cancel this operation or wait 30 seconds to start")
    #time.sleep(30)

    if mode == 0:
        bot.new_auto_mod()

    elif mode == 1:
        check_status(bot)
        while bot.self_following - bot.self_follower > 200:
            unfollow_protocol(bot)
            time.sleep(10 * 60)
            check_status(bot)
        while bot.self_following - bot.self_follower < 400:
            while len(bot.user_info_list) < 50:
                feed_scanner(bot)
                time.sleep(5 * 60)
                follow_protocol(bot)
                time.sleep(10 * 60)
                check_status(bot)

    elif mode == 2:
        bot.bot_mode = 1
        bot.new_auto_mod()

    elif mode == 3:
        unfollow_protocol(bot)
        time.sleep(10 * 60)

    elif mode == 4:
        feed_scanner(bot)
        time.sleep(60)
        follow_protocol(bot)
        time.sleep(10 * 60)

    elif mode == 5:
        bot.bot_mode = 2
        unfollow_protocol(bot)

    else:
        print("Wrong mode!")
'''