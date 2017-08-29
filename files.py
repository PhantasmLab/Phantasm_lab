from pathlib import Path
from os import mknod, makedirs, remove
import csv
from datetime import datetime
from shutil import rmtree

class data:

    def __new__(cls, path):
        cls.path = Path('groups/G{}/'.format(path))
    

    @classmethod
    def create_path_and_check(cls):
        if not cls.path.exists():
            makedirs(cls.path)
        

    @classmethod
    def ban_and_warn_write(cls, user, which):
        with open(cls.path.__str__() + '/{}.txt'.format(which), 'a') as file:
            file.write(user + '\n')
    
    
    @classmethod
    def unban_and_unwarn_back(cls, user_id, which):
        file = open(cls.path.__str__() + '/{}.txt'.format(which), 'r')
        file_read = file.read().split('\n')

        file_write = open(cls.path.__str__() + '/{}.txt'.format(which), 'w')
        if user_id in file_read:
            file_read.remove(user_id)
            for user in file_read:
                file_write.write(user + '\n')
            file.close()

    @classmethod
    def counter_warnings(cls, user_id):
        with open(cls.path.__str__() + '/warn.txt', 'r') as file:
            file_read = file.read().split('\n')
            return file_read.count(user_id)


    @classmethod
    def afk(cls, user):
        a = None
        while 1:
            try:
                if 1:
                    with open(cls.path.__str__() + '/afk.csv') as csv_file:
                        reader = csv.DictReader(csv_file, delimiter=',')
                        afk = [line['afk'] for line in reader]
                        if user in afk:
                            a = False
                        else:
                            with open(cls.path.__str__() + '/afk.csv', 'a') as file:
                                append = csv.writer(file,delimiter=',')
                                append.writerow([user,datetime.now().strftime('%Y/%m/%d %H:%M')])
                            a = True
            except FileNotFoundError:
                with open(cls.path.__str__() + '/afk.csv', 'w') as csv_file:
                    write = csv.writer(csv_file, delimiter=',')
                    write.writerow(['afk','hour'])             
            else:
                break
        return a
        

    @classmethod
    def afklist_and_blacklist(cls, which):
        while 1:
            try:
                if which == 'afk.csv':
                    with open(cls.path.__str__() + '/{}'.format(which)) as file:
                        reader = csv.DictReader(file, delimiter=',')
                        afklist = [line['afk']+'\n' for line in reader]
                        return ''.join(afklist)
                else:
                    with open(cls.path.__str__() + '/{}'.format(which), 'r') as file:
                        return file.read() 
            except FileNotFoundError:
                if which == 'blacklist.txt':
                    mknod(cls.path.__str__() + '/{}'.format(which))
                else:
                    with open(cls.path.__str__() + '/afk.csv', 'w') as csv_file:
                        write = csv.writer(csv_file, delimiter=',')
                        write.writerow(['afk','hour'])      
            else:
                break

    @classmethod
    def clearlist_x(cls, clear):
        clear_dict = {'afk.csv','blacklist.txt','warn.txt'}
        
        if len(clear) > 2:
            for i in clear_dict:
                with open(cls.path.__str__() + '/{}'.format(i), 'w') as limparlista:
                    limparlista.write('')
                return '<b>Selected Lists Clear.</b>'  
        else:
            if 'blacklist' in clear:
                remove(cls.path.__str__() + '/blacklist.txt')
                return '<b>Blacklist clear!</b>' 
        
            elif 'afklist' in clear:
                remove(cls.path.__str__() + '/afk.csv')
                return '<b>Afklist clear!</b>' 
        
            elif 'warn' in clear:
                remove(cls.path.__str__() + '/warn.txt')
                return '<b>warn clear!</b>' 
        
            elif 'all' in clear:
                rmtree(cls.path.__str__() + '/*')
                return '<b>All clear!</b>'
            else: 
                return '<b>Invalid Command, Requires argument.\nTry:</b> /clear blacklist afklist...'

    