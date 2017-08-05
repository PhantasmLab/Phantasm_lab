import telepot
import time
class main:

    def __init__(self, bot, msg):
            
            self.bot = bot
            try:
                self.content_type, self.chat_type, self.chat_id = telepot.glance(msg)
            except:
                self.chat_id, self.chat_type = msg['message']['chat']['id'], msg['message']['chat']['type']
                pass
            self.user = msg['from']['first_name']
            self.username = msg['from']['username']
            self.UserID = msg['from']['id']
            self.msg = msg
            
        
    
    def get_admin_list(self):
        admin = self.bot.getChatAdministrators(self.chat_id)
        AdminID_list = [adminID['user']['id'] for adminID in admin]
        
        if self.UserID in AdminID_list:
            return True
        self.bot.sendMessage(chat_id=self.chat_id,parse_mode='HTML', text=('<b>VOCÊ NÃO TEM PERMISSÃO PARA USAR ESSE COMANDO!!</b>'))


    


class command(main):
    
    def afk(self, text_command):
        motivo = text_command
        afk_open = open('afk.txt', 'a')

        with open('afk.txt', 'r') as afk_open1:
                reader = list(afk_open1.read().split('\n'))
                if self.user in reader:
                    afk_open.close()
                    self.bot.sendMessage(chat_id=self.chat_id, parse_mode='HTML', text='<b>Você Ja esta AFK!</b>')
                    return

        if len(motivo) == 1:
            motivo.append('')
            msgafk = '<b>Usuário {0} está afk!</b>\n<b>Razão</b>: Não especificado.'.format(self.user)
            afk_open.write(self.user+'\n')

        else:
            msgafk = '<b>Usuário {0} está afk!</b>\n<b>Razão</b>: {1}'.format(self.user,motivo[1])
            afk_open.write(self.user+'\n')
        afk_open.close()
        self.bot.sendMessage(chat_id=self.chat_id,parse_mode='HTML', text=msgafk)


    def afklist(self): 
        file = open('afk.txt', 'r')
        f = file.read()
        if list(f) == []:
            self.bot.sendMessage(chat_id=self.chat_id,parse_mode='HTML', text='<b>Nenhum Usuário na lista!</b>')
            return       
        self.bot.sendMessage(chat_id=self.chat_id,text=f)

    def back(self):
        afklist = open('afk.txt', 'r')
        lista = afklist.read().split('\n')
        afklist.close()
        lista.remove(self.user)
        write_afk_list = open('afk.txt', 'w')
        for i in lista:
            write_afk_list.write(i)

        self.bot.sendMessage(chat_id=self.chat_id, parse_mode='HTML', text='<b>Usuário {} está de volta!</b>'.format(self.user))
    
    def clearlists(self, clear):
    
        if 'blacklist' in clear:
            with open('list_ban.txt', 'w') as limparlista:
                limparlista.write('')
                return '<b>Blacklist clear!</b>'
    
        if 'afklist' in clear:
            with open('afk.txt', 'w') as limparlista:
                limparlista.write('')
                return '<b>Afklist clear!</b>'
    
        if 'warn' in clear:
            with open('warn.txt', 'w') as limparlista:
                limparlista.write('')
                return '<b>warn clear!</b>'
    
        if 'all' in clear:
            with open('list_ban.txt', 'w') as limparlista, open('afk.txt', 'w') as limparlista, open ('warn.txt', 'w') as limparlista:
                limparlista.write('')
                return '<b>All clear!</b>'
        return '<b>Comando Invalido, falta de parâmetro.\n Tente:</b> /clear blacklist afklist...'


    def blacklist(self):
        print('aqui')
        with open('list_ban.txt', 'r') as file:
            file_read = file.read()
            if  file_read == '':
                self.bot.sendMessage(parse_mode='HTML',chat_id=self.chat_id,text='<b>Nenhum Usuário na lista!</b>')
                return
            self.bot.sendMessage(parse_mode='HTML',chat_id=self.chat_id,text=file_read)

    def rules(self):
        
        with open('rules.txt', 'r') as file:
            file_read = file.read()
            self.bot.sendMessage(parse_mode='HTML',chat_id=self.chat_id,text=file_read)

    def pin(self):
        self.message_id = self.msg['reply_to_message']['message_id']
        self.bot.pinChatMessage(chat_id=self.chat_id, message_id=self.message_id)
    
    def unpin(self):
        self.bot.unpinChatMessage(chat_id=self.chat_id)

  