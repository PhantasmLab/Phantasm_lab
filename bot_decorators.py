import logging
from datetime import datetime

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
             '/unpin', '/pin', '/afk', '/rules', '@admin','test'
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