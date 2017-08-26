import logging
from datetime import datetime


def log(func):
        
    day_date_hour = datetime.now().strftime('%c')
    logging.basicConfig(filename='.tmp/users_register.log', filemode='w', level=logging.INFO)

    def wrapper(*args,**kwargs):
        if args[0].msg.get('data'):
            return func(*args, **kwargs)
        else:
            resul = func(*args, **kwargs)
            logging.info("log [{}]".format(day_date_hour))
            logging.info(" | Username: {} | ID: {} | Comando usado: {}\n".format(
            args[0].user,
            args[0].UserID, 
            args[0].msg['text'].split(' ')[0]))
        return resul
    return wrapper


def admin(func):
    def wrapper(*args, **kwargs):
        if args[0].msg.get('data'):
            if args[0].get_admin_list(query=True):
                func(*args,**kwargs)
        elif args[0].get_admin_list():
            func(*args,**kwargs)
    return wrapper

def check(func):
    commands = {
            '/ban','/warn','/unwarn','/afklist',	  
            '/admins','/back','/unban', '/blacklist',      
            '/promote','/clear','data','/demote', 'rt', 'rtzao',
             '/unpin', '/pin', '/afk', '/rules', '@admin','/text'
        }
    def wrapper(msg):
        if msg.get('text'):
            if msg['text'].split(' ')[0].lower() in commands:
                func(msg)
        elif msg.get('data'):
            func(msg)
        elif msg.get('new_chat_member'):
            func(msg)
    return wrapper