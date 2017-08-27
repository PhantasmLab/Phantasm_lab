from pathlib import Path
from os import makedirs
from os import mknod

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
    def afk(cls, user=None, listafk=False):
        while 1:
            try:
                if listafk:
                    lista = open(cls.path.__str__() + '/afk.txt', 'r')
                    lista_r = lista.read()
                    lista.close()
                    if user in lista_r:
                        return True
            except FileNotFoundError:
                mknod(cls.path.__str__() + '/afk.txt')
            else:
                break
        
        else:
            return False
        with open(cls.path.__str__() + '/afk.txt', 'a') as file:
            file.write(user+'\n')
    

    @classmethod
    def afklist_and_blacklist(cls, which):
        while 1:
            try:
                with open(cls.path.__str__() + '/{}.txt'.format(which), 'r') as file:
                    return file.read()
            except FileNotFoundError:
                mknod(cls.path.__str__() + '/{}.txt'.format(which))
            else:
                break

    @classmethod
    def clearlist_x(cls, clear):
        clear_dict = {'afklist' : 'afk.txt',
                      'blacklist' : 'list_ban.txt',
                      'warn' : 'warn.txt'
        }
        
        if len(clear) > 2:
            for k in clear_dict.keys():
                with open(cls.path.__str__() + '/{}.txt'.format(clear_dict[k]), 'w') as limparlista:
                    limparlista.write('')
                return '<b>Selected Lists Clear.</b>'  
        else:
            if 'blacklist' in clear:
                with open(cls.path.__str__() + '/blacklist.txt', 'w') as limparlista:
                    limparlista.write('')
                return '<b>Blacklist clear!</b>' 
        
            elif 'afklist' in clear:
                with open(cls.path.__str__() + '/afk.txt', 'w') as limparlista:
                    limparlista.write('')
                return '<b>Afklist clear!</b>' 
        
            elif 'warn' in clear:
                with open(cls.path.__str__() + '/warn.txt', 'w') as limparlista:
                    limparlista.write('')
                return '<b>warn clear!</b>' 
        
            elif 'all' in clear:
                with open(cls.path.__str__() + '/blacklist.txt', 'w') as limparlista, open(cls.path.__str__() + '/afk.txt', 'w') as limparlista, open (cls.path.__str__() + '/warn.txt', 'w') as limparlista:
                    limparlista.write('')
                return '<b>All clear!</b>'
            else: 
                return '<b>Invalid Command, Requires argument.\nTry:</b> /clear blacklist afklist...'
