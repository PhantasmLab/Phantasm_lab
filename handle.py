import telepot
from pathlib import Path
from os import mkdir

from bot_decorators import *
from files import data

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
            data(self.chat_id)
            data.create_path_and_check()
            
        
    
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
    
    def afk(self):
        
        motivo = self.msg['text'][5:]
        if data.afk(self.user):
            if len(motivo) == 0:
                msgafk = '<b>User:</b> <a href="https://telegram.me/{1}/">{0}</a> is now afk!<b>\nReason</b>: Not specified.'.format(self.user, self.username)
                data.afk(self.user)

            else:
                msgafk = '<b>User:</b> <a href="https://telegram.me/{1}/">{0}</a> <b>is now afk!\nReason</b>: {2}'.format(self.user,self.username,motivo)
                data.afk(self.user)
            self.bot.sendMessage(chat_id=self.chat_id,
                                parse_mode='HTML', 
                                text=msgafk, 
                                disable_web_page_preview=True, 
                                reply_to_message_id=self.msg_id)


    @admin
    def afklist(self): 
        resul = data.afklist_and_blacklist('afk.csv')
        if resul == '':
            self.bot.sendMessage(chat_id=self.chat_id,
                                 parse_mode='HTML', 
                                 text='<b>No Users in the list!</b>',
                                 reply_to_message_id=self.msg_id)
            return       
        self.bot.sendMessage(chat_id=self.chat_id,text=resul, reply_to_message_id=self.msg_id)


    def back(self):
        data.unban_and_unwarn_back(self.user, 'afk')
        self.bot.sendMessage(chat_id=self.chat_id, 
                             parse_mode='HTML', 
                             text='<b>User</b> <a href="https://telegram.me/{1}/">{0}</a> <b>is back!</b>'.format(self.user, self.username), 
                             disable_web_page_preview=True,
                             reply_to_message_id=self.msg_id)


    @admin
    def clearlists(self):
        clear = self.msg['text'].split(' ')
        resp = data.clearlist_x(clear)
        self.bot.sendMessage(chat_id=self.chat_id, 
                             parse_mode='HTML', 
                             text=resp,
                             reply_to_message_id=self.msg_id)


    @admin
    def blacklist(self):
        resul = data.afklist_and_blacklist('blacklist.txt')
        if  resul == '':
            self.bot.sendMessage(parse_mode='HTML',
                                 chat_id=self.chat_id,
                                 text='<b>No Users in the list!</b>',
                                 reply_to_message_id=self.msg_id)
            return
        self.bot.sendMessage(parse_mode='Markdown',
                             chat_id=self.chat_id,
                             text=resul,
                             reply_to_message_id=self.msg_id)


    def rules(self):		
        self.bot.sendMessage(parse_mode='HTML',
                             chat_id=self.chat_id,
                             text='<a href="LINK HERE">rules</a>',
                             reply_to_message_id=self.msg_id)


    @admin
    def pin(self):
        message_id = self.msg['reply_to_message']['message_id']
        self.bot.pinChatMessage(chat_id=self.chat_id, message_id=message_id)


    @admin
    def unpin(self):
        self.bot.unpinChatMessage(chat_id=self.chat_id)
    

    @admin
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
        idmsg = self.msg['reply_to_message']['message_id']
        message = self.msg['reply_to_message']['text']
        userresp = self.msg['reply_to_message']['from']['first_name']
        username = self.msg['reply_to_message']['from']['username']
        
        if text is None:
            self.bot.sendMessage(parse_mode='HTML',
                                 chat_id=self.chat_id,
                                 text='🔊 <a href="https://telegram.me/{1}/">{0}</a>' 
                                 'agree with <a href="https://telegram.me/{3}/">{2}</a>!\n\n💬: <b>{4}</b>'.format(
                                 self.user,
                                 self.username,
                                 userresp,
                                 username,
                                 message), 
                                 reply_to_message_id=idmsg, 
                                 disable_web_page_preview=True)

        else:
            self.bot.sendMessage(parse_mode='HTML',
                                 chat_id=self.chat_id,
                                 text='🔊 <a href="https://telegram.me/{1}/">{0}</a> agree with' 
                                 '<a href="https://telegram.me/{3}/">{2}</a>!\n\n💬: <b>{4}</b>\n\n🗯: {5}'.format(
                                 self.user,
                                 self.username,
                                 userresp,
                                 username,
                                 message,
                                 text), 
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
            group,    msg_re      = self.msg['chat']['title'],                        self.msg['reply_to_message']['text']
            id_msg,   user_id     = self.msg['reply_to_message']['message_id'],       self.msg['reply_to_message']['from']['id']
            username, userresp    = self.msg['reply_to_message']['from']['username'], self.msg['reply_to_message']['from']['first_name']
            
            msg = '<b>User</b>: <a href="https://telegram.me/{1}/">{0}</a>' 
            '<b>reported this message:</b>\n\n<i>{2}</i>\n\n<b>User Reported:</b>' 
            '<a href="https://telegram.me/{4}/">{3}</a>\n<b>Id</b>: {5}\n'
            '<b>Message Id</b>: {6}\n<b>From</b>: {7}'.format(self.user,self.username,msg_re,username,username, user_id,id_msg,group)
            
            self.bot.sendMessage(chat_id='ANY ID OF ONE CHANNEL, PM... anything to send the report',
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
