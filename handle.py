import telepot

from bot_decorators import *


class main:

    def __init__(self, bot, msg):
            
            if msg.get('data'):
                self.msg = msg
                self.UserID = msg['from']['id']
                self.chat_id = msg['message']['chat']['id']
                self.chat_type = msg['message']['chat']['type']
                self.query_id, self.from_id, self.query_data = telepot.glance(msg, flavor='callback_query')
                
            else:
                self.msg_id = msg['message_id']	
                self.content_type, self.chat_type, self.chat_id = telepot.glance(msg)
                    
            if msg['from'].get('username'):
                self.username = msg['from']['username']
            else:
                self.username = 'No Username'

            self.bot = bot
            self.msg = msg
            self.UserID = msg['from']['id']
            self.user = msg['from']['first_name']
            
            
            
        
    
    def get_admin_list(self, query=False, user_reply=False):
        admin = self.bot.getChatAdministrators(self.chat_id)
        AdminID_list = [adminID['user']['id'] for adminID in admin]

        if user_reply:
            return AdminID_list

        if self.UserID in AdminID_list:
            return True
        
        if query != False:
            self.bot.answerCallbackQuery(callback_query_id=self.query_id, 
                                         text='You are not allowed to use this button!',
                                         show_alert=False,
                                         cache_time=1)
            return

        self.bot.sendMessage(chat_id=self.chat_id,
                             parse_mode='HTML', 
                             text='<b>YOU DO NOT HAVE PERMISSION TO USE THIS COMMAND!</b>')
    
    def get_creator(self):
        creator = self.bot.getChatAdministrators(self.chat_id)
        creator_id = [c_id['user']['id'] for c_id in creator if c_id['status'] == 'creator']
        

        if self.UserID in creator_id:
            return True
        self.bot.sendMessage(chat_id=self.chat_id,
                             parse_mode='HTML', 
                             text='<b>ONLY THE CREATOR CAN USE THIS COMMAND!</b>', 
                             reply_to_message_id=self.msg_id)
    


    


class command(main):
    
    def afk(self, ):
        motivo = self.msg['text'][5:]
        afk_open = open('afk.txt', 'a')

        with open('afk.txt', 'r') as afk_open1:
                reader = list(afk_open1.read().split('\n'))
                if self.user in reader:
                    afk_open.close()
                    self.bot.sendMessage(chat_id=self.chat_id, 
                                         parse_mode='HTML', 
                                         text='<b>You are already AFK!</b>', 
                                         reply_to_message_id=self.msg_id)
                    return

        if len(motivo) == 0:
            msgafk = '<b>User:</b> <a href="https://telegram.me/{1}/">{0}</a> is afk!<b>\nReason</b>: Not specified.'.format(self.user, self.username)
            afk_open.write(self.user+'\n')

        else:
            msgafk = '<b>User:</b> <a href="https://telegram.me/{1}/">{0}</a> <b>is afk!\nReason</b>: {2}'.format(self.user,
                                                                                             self.username,
                                                                                             motivo)
            afk_open.write(self.user+'\n')
        afk_open.close()
        self.bot.sendMessage(chat_id=self.chat_id,
                             parse_mode='HTML', 
                             text=msgafk, 
                             disable_web_page_preview=True, 
                             reply_to_message_id=self.msg_id)

    @admin
    def afklist(self): 
        file = open('afk.txt', 'r')
        f = file.read()
        if list(f) == []:
            self.bot.sendMessage(chat_id=self.chat_id,
                                 parse_mode='HTML', 
                                 text='<b>No Users in the list!</b>',
                                 reply_to_message_id=self.msg_id)
            return       
        self.bot.sendMessage(chat_id=self.chat_id,text=f, reply_to_message_id=self.msg_id)

    def back(self):
        afklist = open('afk.txt', 'r')
        lista = afklist.read().split('\n')
        afklist.close()
        lista.remove(self.user)
        write_afk_list = open('afk.txt', 'w')
        for i in lista:
            write_afk_list.write(i)

        self.bot.sendMessage(chat_id=self.chat_id, 
                             parse_mode='HTML', 
                             text='<b>User</b> <a href="https://telegram.me/{1}/">{0}</a> <b>is back!</b>'.format(self.user, self.username), 
                             disable_web_page_preview=True,
                             reply_to_message_id=self.msg_id)

    @admin
    @log
    def clearlists(self):
        clear_dict = {'afklist' : 'afk.txt',
                      'blacklist' : 'list_ban.txt',
                      'warn' : 'warn.txt'
        }
        clear = self.msg['text'].split(' ')

        if len(clear) > 2:
            for k in clear_dict.keys():
                with open(clear_dict[k], 'w') as limparlista:
                    limparlista.write('')
            resp = '<b>Selected Lists Clear.</b>'
            return  
        else:
            if 'blacklist' in clear:
                with open('list_ban.txt', 'w') as limparlista:
                    limparlista.write('')
                resp = '<b>Blacklist clear!</b>' 
        
            elif 'afklist' in clear:
                with open('afk.txt', 'w') as limparlista:
                    limparlista.write('')
                resp = '<b>Afklist clear!</b>' 
        
            elif 'warn' in clear:
                with open('warn.txt', 'w') as limparlista:
                    limparlista.write('')
                resp = '<b>warn clear!</b>' 
        
            elif 'all' in clear:
                with open('list_ban.txt', 'w') as limparlista, open('afk.txt', 'w') as limparlista, open ('warn.txt', 'w') as limparlista:
                    limparlista.write('')
                resp = '<b>All clear!</b>'
            else: 
                resp = '<b>Invalid Command, Requires argument.\nTry:</b> /clear blacklist afklist...'
        
        self.bot.sendMessage(chat_id=self.chat_id, 
                             parse_mode='HTML', 
                             text=resp,
                             reply_to_message_id=self.msg_id)

    @admin
    def blacklist(self):
        with open('list_ban.txt', 'r') as file:
            file_read = file.read()
            if  file_read == '':
                self.bot.sendMessage(parse_mode='HTML',
                                     chat_id=self.chat_id,
                                     text='<b>No Users in the list!</b>',
                                     reply_to_message_id=self.msg_id)
                return
            self.bot.sendMessage(parse_mode='Markdown',
                                 chat_id=self.chat_id,
                                 text=file_read,
                                 reply_to_message_id=self.msg_id)


    def rules(self):		
        self.bot.sendMessage(parse_mode='HTML',
                             chat_id=self.chat_id,
                             text='<a href="http://telegra.ph/Division-of-intelligence-08-05">rules</a>',
                             reply_to_message_id=self.msg_id)


    @admin
    @log
    def pin(self):
        message_id = self.msg['reply_to_message']['message_id']
        self.bot.pinChatMessage(chat_id=self.chat_id, message_id=message_id)


    @admin
    @log
    def unpin(self):
        self.bot.unpinChatMessage(chat_id=self.chat_id)
    

    @admin
    @log
    def promote_demote(self, admin=True):
        if self.get_creator():
            adminuser = self.msg['reply_to_message']['from']['first_name']
            self.bot.promoteChatMember(chat_id=self.chat_id, user_id=self.msg['reply_to_message']['from']['id'],
                                       can_change_info=admin, can_post_messages=None, 
                                       can_edit_messages=None, can_delete_messages=admin, 
                                       can_invite_users=admin, can_pin_messages=admin, 
                                       can_promote_members=None, can_restrict_members=admin)

            if admin:
                self.bot.sendMessage(chat_id=self.chat_id, 
                                    text='{0} becames a admin.'.format(adminuser),
                                    reply_to_message_id=self.msg_id)
            else:
                self.bot.sendMessage(chat_id=self.chat_id, 
                                    text='{0} is not more admin.'.format(adminuser),
                                    reply_to_message_id=self.msg_id)


    def rt(self, text=None):
        userresp = self.msg['reply_to_message']['from']['first_name']
        username = self.msg['reply_to_message']['from']['username']
        idmsg = self.msg['reply_to_message']['message_id']
        message = self.msg['reply_to_message']['text']
        
        if text is None:
            self.bot.sendMessage(parse_mode='HTML',
                                 chat_id=self.chat_id,
                                 text='🔊 <a href="https://telegram.me/{1}/">{0}</a> __agree with__ <a href="https://telegram.me/{3}/">{2}</a>!\n\n💬: <b>{4}</b>'.format(self.user,self.username, 
                                                                                                                                             userresp,username,message), 
                                 reply_to_message_id=idmsg, 
                                 disable_web_page_preview=True)

        else:
            self.bot.sendMessage(parse_mode='HTML',
                                 chat_id=self.chat_id,
                                 text='🔊 <a href="https://telegram.me/{1}/">{0}</a> __agree with__ <a href="https://telegram.me/{3}/">{2}</a>!\n\n💬: <b>{4}</b>\n\n🗯: __{5}__'.format(self.user,self.username, 
                                                                                                                                                          userresp,username, 
                                                                                                                                                          message,text), 
                                reply_to_message_id=idmsg, 
                                disable_web_page_preview=True)
    

    def admin(self):
        admin = ['├ '+adminuser['user']['first_name'] + '\n' for adminuser in self.bot.getChatAdministrators(self.chat_id)]
        admins = ''.join(admin[:-1])
        msg = '👤 <b>Creator</b>:\n└{0}\nAdmins:\n{1}'.format(admin[-1][1:], admins)
        self.bot.sendMessage(chat_id=self.chat_id,
                             parse_mode='HTML',
                             text=msg,
                             reply_to_message_id=self.msg_id)
    
    
    def repotadmin(self):
        if self.msg.get('reply_to_message'):
            group = self.msg['chat']['title']
            msg_re = self.msg['reply_to_message']['text']
            userresp = self.msg['reply_to_message']['from']['first_name']
            username = self.msg['reply_to_message']['from']['username']
            user_id = self.msg['reply_to_message']['from']['id']
            id_msg = self.msg['reply_to_message']['message_id']
            msg = '<b>User</b>: <a href="https://telegram.me/{1}/">{0}</a> <b>reported this message:</b>\n\n<i>{2}</i>\n\n<b>User Reported:</b> <a href="https://telegram.me/{4}/">{3}</a>\n<b>Id</b>: {5}\n<b>Message Id</b>: {6}\n<b>From</b>: {7}'.format(self.user,self.username,
                                                                                                                                                                                                                                                            msg_re,username, 
                                                                                                                                                                                                                                                            username, user_id,id_msg,group)
            self.bot.sendMessage(chat_id='-1001099322003',
                                 parse_mode='HTML',
                                 text=msg,
                                 disable_web_page_preview=True)
            self.bot.sendMessage(chat_id=self.chat_id,
                                 parse_mode='Markdown',
                                 text='*User reported to Admin.*',
                                 disable_web_page_preview=True)
        else:
            self.bot.sendMessage(chat_id=self.chat_id, 
                                 text='You need reply this message.',
                                 reply_to_message_id=self.msg_id)  
