import csv
import logging
from datetime import datetime, timedelta
from sql import *
import json



def db_connection(chat_id, user_id,first_name, username):
    return sql_data(
                    sql_connection(host='localhost',user='root',password='pass',db='phantasm_lab'), 
                    chat_id, 
                    user_id, 
                    first_name,
                    username
    )

def admin(func):
    def wrapper(*args, **kwargs):
        if args[0].msg.get('data'):
            if args[0].get_admin_list(query=True):
                func(*args,**kwargs)
        elif args[0].get_admin_list():
            func(*args,**kwargs)
    return wrapper

def anti_flood(func):
    info_users = {}

    def wrapper(msg):
        if msg.get('data'):
            chat_id = msg['message']['chat']['id']
        else:
            chat_id = msg['chat']['id']
             
        if not(chat_id == 'channel'):
            if not(msg.get('new_chat_participant') or msg.get('left_chat_participant')):
                first_name = msg['from']['first_name']
                user_id = msg['from']['id']
                try:
                    username = msg['from']['username']
                except:
                    username = 'no_username'
                FMT = '%H:%M:%S'
                try:
                    msg_id, chat_id = msg['message_id'], msg['chat']['id']
                except:
                    msg_id = None
                    chat_id = None
                db_conn = db_connection(chat_id,user_id,first_name, username)
                        
                if not(info_users.get(user_id)):
                    #db_conn.sql_update('flood_time',datetime.now().strftime("'%s'"%FMT))
                    info_users[user_id] = {
                        'msgid': [msg_id],
                        'floodnumber': 1, 
                        'username': username,
                        'userid': user_id,
                        'time': str(datetime.now().strftime(FMT))
                    }
                    
                else:
                    time = datetime.strptime(datetime.now().strftime(FMT), FMT) - datetime.strptime(info_users[user_id]['time'], FMT)
                    if time <= timedelta(seconds=5):
                        #db_conn.sql_update('flood_time',datetime.now().strftime("'%s'"%FMT))
                        info_users[user_id]['time'] = str(datetime.now().strftime(FMT))
                        info_users[user_id]['msgid'].append(msg_id)
                        info_users[user_id]['floodnumber'] += 1

                        if info_users[user_id]['floodnumber'] == 5:
                            #db_conn.sql_update('flood_time','DEFAULT')
                            msg['ban'] = info_users[user_id]
                            info_users.pop(user_id)     
                    else: 
                        #db_conn.sql_update('flood_time','DEFAULT')
                        info_users.pop(user_id)
                
        func(msg)

    return wrapper
                

def auto_back(commands):
    def auto_backf(func):
        def wrapper(msg):
            if msg.get('data'):
                chat_id = msg['message']['chat']['id']
            else:
                chat_id = msg['chat']['id']

            if not(chat_id == 'channel'):
                if msg.get('text'):
                    if not (msg['text'].split()[0] in commands):
                        chat_id = msg['chat']['id']
                        first_name = msg['from']['first_name']
                        user_id = msg['from']['id']
                        try:
                            username = msg['from']['username']
                        except:
                            username = 'no_username'
                        path = 'groups/G{}/afk.csv'.format(chat_id)
                        db_conn = db_connection(chat_id,user_id,first_name, username)
                        
                        FMT = '%Y-%m-%d %H:%M:%S'

                        if not(db_conn.is_user_afk_or_back('afk')):
                            d = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), FMT) - datetime.strptime(db_conn.get_value('date_time').__str__(), FMT)
                            if d >= timedelta(minutes=1_440):
                                msg['back'] = '{0} is back, after being {1} hour afk'.format(first_name, d)
                                db_conn.sql_afk_back_update('back')
                            elif d >=  timedelta(minutes=60):
                                msg['back'] = '{0} is back, after being {1} hour afk'.format(first_name, str(d).split(':')[0])
                                db_conn.sql_afk_back_update('back')
                            elif d >= timedelta(minutes=10):
                                msg['back'] = '{0} is back, after being {1} minutes afk.'.format(first_name, str(d).split(':')[1])
                                db_conn.sql_afk_back_update('back')
            func(msg)
        return wrapper
    return auto_backf


def ban_vote_monitor(func):
    
    def wrapper(msg):
        if msg.get('data'):
            chat_id = msg['message']['chat']['id']
        else:
            chat_id = msg['chat']['id']
                
        if not(chat_id == 'channel'):
            with open('bot.json', 'r') as file:
                json_file = json.load(file)
                name = json_file['vote_ban']['name']
                time = json_file['vote_ban']['time']
                temp = json_file['vote_ban']['temp']
                msg_id = json_file['vote_ban']['id_msg']
                user_id = json_file['vote_ban']['id_user']
                agree = json_file['vote_ban']['agree']
                user_in_db = json_file['vote_ban']['user_in_db']
                disagree = json_file['vote_ban']['disagree']
                userID = msg['from']['id']
                user = msg['from']['first_name']
                admins = json_file['vote_ban']['admins']
                timevote = json_file['vote_ban']['time_votation']
                FMT = '%H:%M:%S'
                

            if msg.get('data'):
                if msg['data'] in ('agree', 'disagree'):
                    if time != None:
                        if not(time == None):
                            if datetime.strptime(datetime.now().strftime(FMT), FMT) - datetime.strptime(time, FMT) >= timedelta(minutes=int(timevote)):
                                
                                json_file['vote_ban']['time'] = None
                                msg['text'] = None
                                
                                if agree > disagree:
                                    msg['vote_closed'] = [msg_id,'🔴 <b>Votation Closed.</b>\n\n[{agree}] Agree\n[{disagree}] Disagree\n\n{name} is about to be banned by any admin Online.'.format(
                                    agree=agree,
                                    disagree=disagree,
                                    name=name), {'is_user_in_db': user_in_db,'user':name,'user_id':user_id, 'temp':temp}]
                                elif agree == disagree or disagree > agree:
                                    msg['vote_closed'] = [msg_id,"🔴 <b>Votation Closed.</b>\n\n[{agree}] Agree\n[{disagree}] Disagree\n\n{name} won't be banned.".format(
                                    agree=agree,
                                    disagree=disagree,
                                    name=name), {'is_user_in_db': False,'user':name,'user_id':user_id, 'temp':temp}]
                            else:
                                if userID in admins:
                                    if not(userID in json_file['vote_ban']['voted']):
                                        if msg['data'] == 'agree':
                                            json_file['vote_ban']['agree'] += 1
                                            json_file['vote_ban']['voted'].append(userID)
                                        else:
                                            json_file['vote_ban']['disagree'] += 1
                                            json_file['vote_ban']['voted'].append(userID)
                                                        
                                        msg_vote = '<b>{0}</b> has opened a votation to ban <b>{1}</b>.\n\n<b>TempBan</b>: {2}h\n[{3}] <b>Agree</b>\n[{4}] <b>Disagree</b>\n\n Votation will be closed in {5}min'.format(
                                        user, 
                                        name, 
                                        temp, 
                                        json_file['vote_ban']['agree'],
                                        json_file['vote_ban']['disagree'],
                                        json_file['vote_ban']['time_votation'])
                                        msg['vote_msg'] = [msg_id,msg_vote]

                                        with open('bot.json', 'w') as file:
                                            json.dump(json_file, file, sort_keys=True, indent=4)
                                    else:
                                        msg['vote_query'] = [msg_id]
                                else:
                                    msg['permission'] = True                
            else:
                if not(json_file['vote_ban']['time'] == None):
                    if datetime.strptime(datetime.now().strftime(FMT), FMT) - datetime.strptime(time, FMT) >= timedelta(minutes=int(timevote)):
                        
                        json_file['vote_ban']['time'] = None
                        msg['text'] = None

                        if agree > disagree:
                            msg['vote_closed'] = [msg_id,'🔴 <b>Votation Closed.</b>\n\n[{agree}] Agree\n[{disagree}] Disagree\n\n{name} is about to be banned by any admin Online.'.format(
                            agree=agree,
                            disagree=disagree,
                            name=name), {'is_user_in_db': user_in_db,'user':name,'user_id':user_id, 'temp':temp}]
                        elif agree == disagree or disagree > agree:
                            msg['vote_closed'] = [msg_id,"🔴 <b>Votation Closed.</b>\n\n[{agree}] Agree\n[{disagree}] Disagree\n\n{name} won't be banned.".format(
                            agree=agree,
                            disagree=disagree,
                            name=name), {'is_user_in_db': False,'user':name,'user_id':user_id, 'temp':temp}]

                        with open('bot.json', 'w') as file:
                            json.dump(json_file, file, sort_keys=True, indent=4)
        func(msg)
             
    return wrapper



def check(func):
    commands = (	  
            '/admins','/back','/unban', '/blacklist',      
            '/promote','/clear','/voteban','data','/demote', 'rt',
            '/ban','/warn','/unwarn','/afklist','/test','rtzao',
            '/unpin', '/uptime','/pin', '/afk', '/rules', '/help'
    )
    FMT = '%Y-%m-%d %H:%M:%S'

    @ban_vote_monitor
    @auto_back(commands)
    @anti_flood
    def wrapper(msg):
        with open('bot.json', 'r') as file:
            json_file = json.load(file)
            time = json_file['article']['time']

        if msg.get('text'):
            if msg['text'].split()[0].lower() in commands:
                func(msg)

        if msg.get('ban') or msg.get('vote_msg') or msg.get('vote_query') or msg.get('vote_closed') or msg.get('back') or msg.get('permission'):
            func(msg)
        
        if datetime.strptime(datetime.now().strftime(FMT), FMT) - datetime.strptime(time, FMT) >= timedelta(minutes=60):
            json_file['article']['time'] = datetime.now().strftime(FMT)
            msg['article'] = True
            with open('bot.json', 'w') as file:
                json.dump(json_file, file, sort_keys=True, indent=4)
            func(msg)
            
        elif msg.get('data'):
            func(msg)
        elif msg.get('new_chat_participant'):
            func(msg)
        
        
    return wrapper
