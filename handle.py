import telepot

class main:

    def __init__(self, bot, msg):
            
            self.bot = bot
            if msg.get('data'):
                self.query_id, self.from_id, self.query_data = telepot.glance(msg, flavor='callback_query')
                self.chat_id = msg['message']['chat']['id']
                self.chat_type = msg['message']['chat']['type']
            else:
                self.content_type, self.chat_type, self.chat_id = telepot.glance(msg)


            self.user = msg['from']['first_name']
            self.username = msg['from']['username']
            self.UserID = msg['from']['id']
            self.msg = msg
            self.msg_id = msg['message_id']
        
    
    def get_admin_list(self, query=False):
        admin = self.bot.getChatAdministrators(self.chat_id)
        AdminID_list = [adminID['user']['id'] for adminID in admin]

        if self.UserID in AdminID_list:
            return True
        
        if query != False:
            self.bot.answerCallbackQuery(callback_query_id=self.query_id, 
                                         text='You are not allowed to use this button!',
                                         show_alert=True,
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
            msgafk = '*User:* [{0}](https://telegram.me/{1}/) is afk!*\nReason*: Not specified.'.format(self.user, self.username)
            afk_open.write(self.user+'\n')

        else:
            msgafk = '*User:* [{0}](https://telegram.me/{1}/) *is afk!\nReason*: {2}'.format(self.user,self.username,motivo)
            afk_open.write(self.user+'\n')
        afk_open.close()
        self.bot.sendMessage(chat_id=self.chat_id,
                             parse_mode='Markdown', 
                             text=msgafk, 
                             disable_web_page_preview=True, 
                             reply_to_message_id=self.msg_id)


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
                             parse_mode='Markdown', 
                             text='*User* [{0}](https://telegram.me/{1}/) *is back!*'.format(self.user, self.username), 
                             disable_web_page_preview=True,
                             reply_to_message_id=self.msg_id)
    
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
                resp = '<b>Invalid Command, Requires argument.\n Try:</b> /clear blacklist afklist...'
        
        self.bot.sendMessage(chat_id=self.chat_id, 
                        parse_mode='HTML', 
                        text=resp,
                        reply_to_message_id=self.msg_id)

    def blacklist(self):
        with open('list_ban.txt', 'r') as file:
            file_read = file.read()
            if  file_read == '':
                self.bot.sendMessage(parse_mode='HTML',
                                     chat_id=self.chat_id,
                                     text='<b>No Users in the list!</b>',
                                     reply_to_message_id=self.msg_id)
                return
            self.bot.sendMessage(parse_mode='HTML',
                                 chat_id=self.chat_id,
                                 text=file_read,
                                 reply_to_message_id=self.msg_id)

    def rules(self):
        
        self.bot.sendMessage(parse_mode='Markdown',
                             chat_id=self.chat_id,
                             text='[rules](http://telegra.ph/Division-of-intelligence-08-05)',
                             reply_to_message_id=self.msg_id)

    def pin(self):
        message_id = self.msg['reply_to_message']['message_id']
        self.bot.pinChatMessage(chat_id=self.chat_id, message_id=message_id)
    
    def unpin(self):
        self.bot.unpinChatMessage(chat_id=self.chat_id)
    
    def promote_demote(self, admin=True):
        if self.get_creator():
            adminuser = self.msg['reply_to_message']['from']['first_name']
            self.bot.promoteChatMember(chat_id=self.chat_id, user_id=self.msg['reply_to_message']['from']['id'],
                                       can_change_info=admin, can_post_messages=None, 
                                       can_edit_messages=None, can_delete_messages=admin, 
                                       can_invite_users=admin, can_pin_messages=admin, 
                                       can_promote_members=None, can_restrict_members=admin)

            if admin:
                self.bot.sendMessage(chat_id=main_inst.chat_id, 
                                    text='{0} becames a admin.'.format(adminuser),
                                    reply_to_message_id=self.msg_id)
            else:
                self.bot.sendMessage(chat_id=main_inst.chat_id, 
                                    text='{0} is not more admin.'.format(adminuser),
                                    reply_to_message_id=self.msg_id)

    def rt(self, text=None):
        userresp = self.msg['reply_to_message']['from']['first_name']
        username = self.msg['reply_to_message']['from']['username']
        idmsg = self.msg['reply_to_message']['message_id']
        message = self.msg['reply_to_message']['text']
        
        if text is None:
            self.bot.sendMessage(parse_mode='Markdown',
                                 chat_id=self.chat_id,
                                 text='🔊 [{0}](https://telegram.me/{1}/) __agree with__ [{2}](https://telegram.me/{3}/)!\n\n💬: *{4}*'.format(self.user,self.username, userresp, username, message), 
                                 reply_to_message_id=idmsg, 
                                 disable_web_page_preview=True)

        else:
            self.bot.sendMessage(parse_mode='Markdown',
                                chat_id=self.chat_id,
                                text='🔊 [{0}](https://telegram.me/{1}/) __agree with__ [{2}](https://telegram.me/{3}/)!\n\n💬: *{4}*\n\n🗯: __{5}__'.format(self.user,self.username, userresp, username, message, text), 
                                reply_to_message_id=idmsg, 
                                disable_web_page_preview=True)
    
    def admin(self):
        admin = ['@' + adminuser['user']['username'] + '\n' for adminuser in self.bot.getChatAdministrators(self.chat_id)]
        self.bot.sendMessage(chat_id=self.chat_id, 
                             text=''.join(admin),
                             reply_to_message_id=self.msg_id)
    
    def repotadmin(self):
        if self.msg.get('reply_to_message'):
            group = self.msg['chat']['title']
            msg_re = self.msg['reply_to_message']['text']
            userresp = self.msg['reply_to_message']['from']['first_name']
            username = self.msg['reply_to_message']['from']['username']
            user_id = self.msg['reply_to_message']['from']['id']
            id_msg = self.msg['reply_to_message']['message_id']
            msg = '*User*: [{0}](https://telegram.me/{1}/) *reported this message:*\n\n`{2}`\n\n*User Reported:* [{3}](https://telegram.me/{4}/)\n*Id*: {5}\n*Message Id*: {6}\n*From*: {7}'.format(self.user,self.username,msg_re,  username, username, user_id,id_msg,group)
            self.bot.sendMessage(chat_id='-1001099322003',
                                 parse_mode='Markdown',
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
    
