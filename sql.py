import pymysql.cursors
from datetime import datetime


class sql_connection:
    
    @classmethod
    def __init__(cls, **kw):
        
        cls.kw = kw
        while 1:
            try:
                cls.connection = pymysql.connect( **cls.kw,
                                                 charset='utf8mb4',
                                                 cursorclass=pymysql.cursors.DictCursor)
            except pymysql.err.InternalError:
                cls.create_db()
            else:
                break

    
    @classmethod
    def get_cursor(cls):
        return cls.connection.cursor()
        
    
    @classmethod
    def create_db(cls):
        sql = 'CREATE DATABASE phantasm_lab CHARACTER SET UTF8 COLLATE utf8_bin'
        cls.kw.pop('db')
        connection = pymysql.connect(**cls.kw,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        cursor.execute(sql)
        cls.kw['db'] = 'phantasm_lab'
        connection.commit()

        

class sql_data:
    
    command = {
        'select': 'SELECT * from {table} WHERE {where}',
        'create_table': "CREATE TABLE IF NOT EXISTS {table} (id int NOT NULL,"
                                              "first_name varchar(255) NOT NULL,"
                                              "username varchar(255) NOT NULL,"
                                              "warn int DEFAULT '0' NOT NULL,"
                                              "ban boolean DEFAULT '0' NOT NULL,"
                                              "afk enum('afk','back'),"
                                              "date_time datetime,"
                                              "PRIMARY KEY(id)) DEFAULT CHARSET = utf8",
        'update': "UPDATE {table} SET {column} = {value} WHERE id = {user_id}",
        'insert_default': "INSERT INTO {table}" 
        "(id,first_name, username)"
        " VALUES ({id}, {first_name}, {username})",
        'update_afk': "UPDATE {table} SET afk = {status}, date_time = {date} WHERE id = {user_id}",
        'clean_values1': "UPDATE {table} SET {column} = {value}",
        'clean_values2': "UPDATE {table} SET {column1} = {value1}, {column2} = {value2}, {column3} = {value3}"
        
    }

    
    def __init__(self, 
                 database, 
                 idgroup, 
                 user_id, 
                 first_name,
                 username):

        self.cursor = database.get_cursor()
        self.database = database
        self.commit = database.connection.commit
        self.id_group = "`g{}`".format(idgroup)
        self.command = sql_data.command
        self.data = {
                    'table': self.id_group,
                    'username': "'%s'" % username,
                    'id': user_id, 
                    'first_name': "'%s'" % first_name, 
        }

    def get_value(self, column,user=None):
        if user != None:
            self.data['id'] = user

        while 1:
            if self.if_table_exist():
                self.cursor.execute(
                    self.command['select'].format(
                        table=self.id_group,
                        where='id = {}'.format(self.data['id'])
                    )
                )
                 
                for row in self.cursor:
                    return row[column]
            else:
                self.ger_table()
    
    def get_id(self, column, user):
        if user != None:
            self.data['id'] = user

        while 1:
            if self.if_table_exist():
                self.cursor.execute(
                    self.command['select'].format(
                        table=self.id_group,
                        where='username = {}'.format(self.data['id'])
                    )
                )
                 
                for row in self.cursor:
                    return row[column]
            else:
                self.ger_table()

        


    def auth_if_user_exist(self, user_id=None, first_name=None):
        if user_id != None:
            self.data['id'] = user_id
        
        #int(self.data['id'])
        self.cursor.execute(
            self.command['select'].format(
                table=self.id_group,
                where=self.data['id']
            )
        )

        if first_name != None and user_id != None:
            self.data['id'] = first_name
        
        try:
            if self.data['id'].isdigit():
                self.data['id'] = int(self.data['id'])
        except AttributeError:
            pass
            
        for row in self.cursor:
            if self.data['id'] in row.values():
                return True
        return False

    
    def if_table_exist(self):
        while 1:
            try:
                self.cursor.execute(
                    'show tables;'
                )
            except pymysql.err.ProgrammingError:
                self.cursor = self.database.get_cursor()
            else:
                break

        for row in self.cursor.fetchall():
            if row['Tables_in_phantasm_lab'] == self.id_group.rstrip('`')[1:]:
                return True
        return False
        


    def sql_warn_and_unwarn(self,
                            user_id,
                            first_name=None,
                            username=None, 
                            quanti=1, 
                            remove=False):

        self.insert_if_not_exists(
            self.data,
            user_id=user_id,
            first_name=first_name,
            username=username
        )
        try:
            if not remove:
                quanti += int(self.get_value('warn',user_id))
            else:
                if not(self.get_warnings(user_id) < 1):
                    quanti = self.get_value('warn',user_id) - quanti
                else:
                    quanti = 0

            self.cursor.execute(
                self.command['update'].format(
                    table=self.id_group, 
                    column='warn',
                    value=quanti, 
                    user_id=user_id
                )
            )
            self.commit()
        finally:
            self.cursor.close()


    def sql_afk_back_update(self, status):
        self.insert_if_not_exists(self.data)

        try:
            self.cursor.execute(
                self.command['update_afk'].format(
                    table=self.id_group, 
                    status="'%s'" % status, #afk or back
                    date="'%s'" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                    user_id=self.data['id']
                )
            )
            self.commit()
        finally:
            self.cursor.close()


    def ger_table(self):
        self.cursor.execute(
            self.command['create_table'].format(
                table=self.id_group
            )
        )
        self.commit()

    

    def insert_if_not_exists(self, kw=None, user_id=None, first_name=None, username=None):
        if kw == None:
            kw = self.data

        if user_id != None and first_name != None and username != None:
            kw['id'] = user_id
            kw['first_name'] = "'%s'" % first_name
            kw['username'] = "'%s'" % username
        
        while 1:
            if self.if_table_exist():
                if not(self.auth_if_user_exist(kw['id'])):
                    self.cursor.execute(
                        self.command['insert_default'].format(
                            **kw
                        )
                    )
                    self.commit()
                break
                        
            else:
                self.ger_table()
    
    def is_banned(self, user_id):
        r = self.get_value('ban',user_id)
        return r == 1
    

    def sql_update(self, 
                   column, 
                   value, 
                   user_id=None, 
                   first_name=None,
                   username=None):

        if user_id != None:
            self.data['id'] = user_id
            self.data['first_name'] = "'%s'" % first_name
            self.data['username'] = "'%s'" % username

        self.insert_if_not_exists(
            self.data, 
            user_id=user_id,
            first_name=first_name,
            username=username
        )

        
        try:
            self.cursor.execute(
                self.command['update'].format(
                    table=self.id_group, 
                    column=column, 
                    value=value, 
                    user_id=self.data['id']
                )
            )
            self.commit()
        finally:
            self.cursor.close()


    def is_user_afk_or_back(self, status):
        while 1:
            if self.if_table_exist():
                if self.auth_if_user_exist(self.data['id']):
                    
                    return not self.get_value('afk') == status
                else:
                    self.insert_if_not_exists(self.data)
                
            else:
                self.ger_table()



    def get_lists(self, to_return):
        string_users = ''
        list_users = ''
        if to_return == 'afk':
            #afk users
            where = 'afk'
        else:
            #banned users
            where = '1' 

        self.cursor.execute(
            self.command['select'].format(
                table=self.id_group,
                where=where
            )
        )
        
        for row in self.cursor:
            if row[to_return] == where: #afk or ban
                string_users += '%s\n' % row['first_name']
        
        return string_users


    def get_warnings(self, user_id):
        self.cursor = self.database.get_cursor()
        self.cursor.execute(
            self.command['select'].format(
                table=self.id_group,
                where='id = {}'.format(user_id)
            )
        )
        for row in self.cursor:
            return row['warn']

  

    def clear_values(self, clear):
        clear_list = {
            'blacklist' : ('<b>Blacklist clear!</b>', ['ban', 'DEFAULT']),
            'afklist'   : ('<b>Afklist clear!</b>', ['afk', "'None'"]),
            'warn'      : ('<b>warn clear!</b>', ['warn', 'DEFAULT']),
            'all'       : '<b>All clear!</b>',
            'selected'  : {'afklist' : ['afk',"'None'"], 
                           'blacklist' : ['ban','DEFAULT'], 
                           'warn' : ['warn','DEFAULT']
                        }
        }

        if len(clear) > 2:
            for k,v in clear_list['selected'].items():

                if k in clear:
                    self.cursor.execute(
                        self.command['clean_values1'].format(
                            table=self.id_group, 
                            column=v[0], 
                            value=v[1]
                        )
                    )
            self.commit()
            return '<b>Selected Lists Clear.</b>'
            
        elif len(clear) == 2:
            if clear_list.get(clear[1]) and clear[1] != 'all':
                self.cursor.execute(
                        self.command['clean_values1'].format(
                            table=self.id_group, 
                            column=clear_list[clear[1]][1][0], 
                            value=clear_list[clear[1]][1][1]
                        )
                    )
                self.commit()
                return clear_list[clear[1]][0]
            else:
                
                self.cursor.execute(
                        self.command['clean_values2'].format(
                            table=self.id_group, 
                            colum1='warn', 
                            value1=0,
                            column2='afk', 
                            value2=None,
                            column3='ban', 
                            value3=0
                        )
                    )
                self.commit()
                return clear_list['all']

        else:
            return '<b>Invalid Command, Requires argument.'
            '\nTry:</b> /clear blacklist afklist...'
    
    def show_tables(self):
        
        self.cursor.execute('SHOW TABLES;')
        print([table['Tables_in_phantasm_lab'][1:] for table in self.cursor])
        return [table['Tables_in_phantasm_lab'][1:] for table in self.cursor]