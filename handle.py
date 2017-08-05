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
            msgafk = '*Usuário:* [{0}](https://telegram.me/{1}/) está afk!*\nRazão*: Não especificado.'.format(self.user, self.username)
            afk_open.write(self.user+'\n')

        else:
            msgafk = '*Usuário:* [{0}](https://telegram.me/{1}/) *está afk!\nRazão*: {2}'.format(self.user,self.username,motivo[1])
            afk_open.write(self.user+'\n')
        afk_open.close()
        self.bot.sendMessage(chat_id=self.chat_id,parse_mode='Markdown', text=msgafk, disable_web_page_preview=True)


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

        self.bot.sendMessage(chat_id=self.chat_id, parse_mode='Markdown', text='*Usuário* [{0}](https://telegram.me/{1}/) *está de volta!*'.format(self.user, self.username), disable_web_page_preview=True)
    
    def clearlists(self, clear):
        clear_dict = {'afklist' : 'afk.txt',
                      'blacklist' : 'list_ban.txt',
                      'warn' : 'warn.txt'
        }

        if len(clear) > 2:
            for k in clear_dict.keys():
                with open(clear_dict[k], 'w') as limparlista:
                    limparlista.write('')
            return '<b>Selected Lists Clear.</b>' 
        else:
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
    
    def promote_demote(self, admin=True):
        self.adminuser = self.msg['reply_to_message']['from']['first_name']
        self.bot.promoteChatMember(chat_id=self.chat_id, user_id=self.msg['reply_to_message']['from']['id'],
                                   can_change_info=admin, can_post_messages=None, 
                                   can_edit_messages=None, can_delete_messages=admin, 
                                   can_invite_users=admin, can_pin_messages=admin, 
                                   can_promote_members=None, can_restrict_members=admin)
    
    def link(self):
        return self.bot.exportChatInviteLink(self.chat_id)
    
    


  