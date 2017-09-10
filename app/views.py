#!flask/bin/python
# -*- coding: utf-8 -*-
import time
import os

from src.check_status import check_status
from src.feed_scanner import feed_scanner
from src.follow_protocol import follow_protocol
from src.instabot import InstaBot
from src.unfollow_protocol import unfollow_protocol
from src.stoppable_thread import StoppableThread

from app import app
from flask import render_template, flash, request, redirect, url_for
from .forms import LoginForm, ControlPanelForm

bot = None
thread = None


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global bot, thread

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
        thread = StoppableThread(target=runBot)
        thread.daemon = True
        thread.start()
        flash('Bot is running!')
        return redirect(url_for('mybot'))

    return render_template('index.html', title='InstabotWebApp', form=form)


@app.route('/mybot', methods=['GET', 'POST'])
def mybot():
    global bot, thread
    form = ControlPanelForm()
    if request.method == 'POST':
        if form.refresh.data and bot:
            with open(bot.log_full_path, 'r') as log:
                for line in log:
                    flash(line)
            return redirect(url_for('mybot'))
        elif form.logout.data and bot:
            os.remove(bot.log_full_path)
            bot.exit_no_cleanup()
            thread.stop()
            flash('Bot stopped!')
            return redirect(url_for('index'))
        else:
            flash('Something went wrong... Please log in again')
            return redirect(url_for('index'))

    return render_template('mybot.html',
                           title='Instabot Control Panel',
                           form=form)


def runBot():

    global bot, thread

    while True:

        if thread:
            if thread.stopped():
                thread.join()

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
