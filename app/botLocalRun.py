from app.src.check_status import check_status
from app.src.feed_scanner import feed_scanner
from app.src.follow_protocol import follow_protocol
from app.src.instabot import InstaBot
from app.src.unfollow_protocol import unfollow_protocol

bot = InstaBot(login='dmtriy.taranov',
               password='Do#@4S84&f',
               like_per_day=1,
               comments_per_day=1,
               follow_per_day=2)


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