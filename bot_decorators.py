import logging
from datetime import datetime, timedelta
import csv



def admin(func):
    def wrapper(*args, **kwargs):
        if args[0].msg.get('data'):
            if args[0].get_admin_list(query=True):
                func(*args,**kwargs)
        elif args[0].get_admin_list():
            func(*args,**kwargs)
    return wrapper

def auto_back(func):
    
    def del_row(path, user):
        with open(path) as csv_file:
            r = [ line for line in csv.reader(csv_file, delimiter=',') if user not in line]
            print(r)
        with open(path, 'w') as csv_file:
            w = csv.writer(csv_file, delimiter=',')
            for line in r:
                w.writerow(line)

    def wrapper(msg):
        if msg.get('text'):
            if msg['text'] != '/afk':

                chat_id = msg['chat']['id']
                first_name = msg['from']['first_name']
                path = 'groups/G{}/afk.csv'.format(chat_id)

                with open(path) as csv_file:
                    reader = csv.DictReader(csv_file, delimiter=',')
                    FMT = '%Y/%m/%d %H:%M'

                    for line in reader:
                        
                        if first_name == line['afk']:
                            d = datetime.strptime(datetime.now().strftime('%Y/%m/%d %H:%M'), FMT) - datetime.strptime(line['hour'], FMT)

                            if d >= timedelta(minutes=1_440):
                                msg['back'] = '{0} is back, after being {1} hour afk'.format(first_name, d)
                                del_row(path,first_name)
                            elif d >=  timedelta(minutes=60):
                                print(d)
                                msg['back'] = '{0} is back, after being {1} hour afk'.format(first_name, str(d)[:-6])
                                del_row(path,first_name)
                                break
                            elif d >= timedelta(minutes=10):
                                print(d)
                                msg['back'] = '{0} is back, after being {1} minutes afk.'.format(first_name, str(d).split(':')[1])
                                del_row(path,first_name)
                                break
                func(msg)
            else:
                func(msg)

        else:
            func(msg)
    return wrapper

def check(func):
    commands = {
            '/ban','/warn','/unwarn','/afklist',	  
            '/admins','/back','/unban', '/blacklist',      
            '/promote','/clear','data','/demote', 'rt', 'rtzao',
             '/unpin', '/pin', '/afk', '/rules', '@admin','test'
        }
    @auto_back
    def wrapper(msg):
        if msg.get('text'):
            if msg['text'].split(' ')[0].lower() in commands:
                func(msg)
            elif msg.get('back'):
                func(msg)
        elif msg.get('data'):
            func(msg)
        elif msg.get('new_chat_member'):
            func(msg)
        
    return wrapper


