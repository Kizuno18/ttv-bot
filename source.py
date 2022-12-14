import multiprocessing
import bot
import time
import random
from settings import settings

 
cookies = bot.GetAllCookies()
proxies = bot.GetProxyList(settings["proxy_type"])
should_mute = True

bot_instances = []

def BotStarter(id,cookie_override):
    if len(proxies) > 0:
        proxy = proxies[random.randint(0,len(proxies)-1)]
        proxies.remove(proxy)
    else:
        print("[!][!][!] You are out of proxies, bots from now on will start without a proxy...")
        proxy = ""
    if cookie_override == None:
        if len(cookies) > 0:
            cookie = cookies[random.randint(0,len(cookies)-1)]
            cookies.remove(cookie)

            process = multiprocessing.Process(target=bot.SpawnBot,args=(cookie,proxy,should_mute))
        else:
            process = multiprocessing.Process(target=bot.SpawnBot,args=(None,proxy,should_mute))
            cookie = None
            
    else:
        process = multiprocessing.Process(target=bot.SpawnBot,args=(cookie_override,proxy,should_mute))
        cookie = cookie_override
    process.start()
    bot_instances.append([process,id,cookie])



if __name__ == "__main__":


    #clean bots_active file

    with open("tools/chatting/active_bots.txt","w") as f:
        f.write("")

    if settings["speech_recognition"] == "yes":
        should_mute = False
    for i in range(int(settings["bots"])):
        BotStarter(i,None)
        time.sleep(random.randint(1,10) * int(settings["bot_spawn_rate"]))
        should_mute = True
    
    while True:
        for i in range(int(settings["bots"])):
            if bot_instances[i][0].is_alive() == False:
                print("[!] Bot has died...","Restarting with cookie",bot_instances[i][2])
                bot_instances[i][0].close()
                if bot_instances[i][2] != None:
                    BotStarter(bot_instances[i][1],bot_instances[i][2])
                else:
                    BotStarter(bot_instances[i][1],None)
                bot_instances.remove(bot_instances[i])

        time.sleep(1)

