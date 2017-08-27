from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

from files import data
from bot_decorators import *
from handle import main


class punish(main):
    
    def __init__(self, bot, msg):
        super().__init__(bot,msg)
        
        if self.msg.get('text'):
            if self.msg['text'].split(' ')[0].lower() in ['/ban', '/unban', '/warn', '/unwarn']:
                self.userresp = self.msg['reply_to_message']['from']['first_name']               
                self.user_id = str(self.msg['reply_to_message']['from']['id'])
                self.message_id = self.msg['reply_to_message']['message_id']
                if msg['reply_to_message'].get('username'):
                    self.usernamerep = self.msg['reply_to_message']['from']['username']
                else:
                    self.usernamerep = 'No username'
    

        

    @admin			
    def ban(self, warn=False):
        data.create_path_and_check()

        if self.user_id in str(self.get_admin_list(user_reply=True)):
            self.bot.sendMessage(chat_id=self.chat_id, 
                                parse_mode='HTML', 
                                text="<b>You can't ban a ADMIN!</b>",
                                reply_to_message_id=self.msg_id)
            return None
        self.bot.kickChatMember(self.chat_id,self.user_id)
        if warn:
            self.bot.sendMessage(chat_id=self.chat_id, 
                                     parse_mode='HTML', 
                                     text='<a href="https://telegram.me/{1}/">{0}</a> <b>banned:</b> reached the max number of warnings (<b>3/3</b>)'.format(self.userresp, self.usernamerep), 
                                     disable_web_page_preview=True,
                                     reply_to_message_id=self.msg_id)
            with open('list_ban.txt', 'a') as list_ban:
                list_ban.write('<i>' + self.userresp + '<i>'+'\n')
            return
        #add list
        data.ban_and_warn_write(self.userresp, 'blacklist')

        
        self.bot.sendMessage(chat_id=self.chat_id, 
                             parse_mode='HTML', 
                             text='<b>sudo rm -rf</b> <a href="https://telegram.me/{1}/">{0}</a>'.format(self.userresp,self.usernamerep), 
                             disable_web_page_preview=True,
                             reply_to_message_id=self.msg_id)
        d = open('ban.mp4', 'rb')
        self.bot.sendVideoNote(self.chat_id, video_note=d)
        d.close()

    @admin
    def unban(self):
        self.bot.unbanChatMember(self.chat_id, self.user_id)
        self.bot.sendMessage(chat_id=self.chat_id, 
                             parse_mode='HTML', 
                             text='<a href="https://telegram.me/{1}/">{0}</a> <b>unbanned by</b> <a href="https://telegram.me/{3}/">{2}</a>'.format(self.userresp,self.usernamerep, 
                                                                                                                            self.user, self.username), 
                             disable_web_page_preview=True,
                             reply_to_message_id=self.msg_id)                         
        data.unban_and_unwarn_back(self.user_id, 'blacklist')


    @admin	
    def warn(self, quanti):
        data.create_path_and_check()

        if len(quanti) > 1:
            quanti[1] = int(quanti[1])
            for warn_qt in range(quanti[1]):
                data.ban_and_warn_write(self.user_id, 'warn')
        else:
            data.ban_and_warn_write(self.user_id, 'warn')
        
        if data.counter_warnings(self.user_id) >= 3:
            print(data.counter_warnings(self.user_id))
            retur = self.ban(warn=True)
            return
        
        cont = data.counter_warnings(self.user_id)
        
        self.bot.sendMessage(chat_id=self.chat_id, 
                             parse_mode='HTML', 
                             text='<a href="https://telegram.me/{1}/">{0}</a> <b>has been warned</b> (<i>{2}</i>/<b>3</b>)'.format(self.userresp, self.usernamerep,cont), 
                             reply_markup=self.keyboard_warn(), 
                             disable_web_page_preview=True,
                             reply_to_message_id=self.msg_id)


    @admin						 
    def unwarn(self, **keyword):
        print('unwarn')
        if keyword.get('data', False):
                self.bot.answerCallbackQuery(callback_query_id=self.query_id, 
                                             text='Warn has been removed!',
                                             show_alert=False,
                                             cache_time=1)
                data.unban_and_unwarn_back(keyword['data'], 'warn')
        else:
            data.unban_and_unwarn_back(self.user_id, 'warn')


    def keyboard_warn(self):
        return InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="Remove Warn", callback_data=str(self.user_id))]
                    ])
