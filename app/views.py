#!flask/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import threading

sys.path.append(os.path.join(sys.path[0], 'src'))

from src.check_status import check_status
from src.feed_scanner import feed_scanner
from src.follow_protocol import follow_protocol
from src.instabot import InstaBot
from src.unfollow_protocol import unfollow_protocol

from app import app
from flask import render_template, flash, request, redirect, url_for
from .forms import LoginForm, LogoutForm

bot = None

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global bot
    form = LoginForm()
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        like_per_day = int(request.form['like_per_day'])
        comments_per_day = int(request.form['comments_per_day'])
        follow_per_day = int(request.form['follow_per_day'])
        bot = InstaBot(
            login=login,
            password=password,
            like_per_day=like_per_day,
            comments_per_day=comments_per_day,
            follow_per_day=follow_per_day)
        t = threading.Thread(target=runBot)
        t.start()
        flash('Bot is running!')
        return redirect(url_for('logout'))

    return render_template('index.html', title='InstabotWebApp', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global bot
    form = LogoutForm()
    if request.method == 'POST':
        stopBot()
        flash('Bot stopped!')
        return redirect(url_for('index'))

    return render_template('logout.html', title='Logout from Instabot', form=form)

def runBot():

    global bot

    while True:

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


def stopBot():
    global bot
    bot.logout()
