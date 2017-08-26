from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

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
        else:
            self.userresp = None
            self.user_id = None
            self.message_id = None

        

    @admin			
    @log
    def ban(self, warn=False):
        #ban user
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
        with open('list_ban.txt', 'a') as list_ban:
            list_ban.write(self.userresp+'\n')

        
        self.bot.sendMessage(chat_id=self.chat_id, 
                             parse_mode='HTML', 
                             text='<b>sudo rm -rf</b> <a href="https://telegram.me/{1}/">{0}</a>'.format(self.userresp,self.usernamerep), 
                             disable_web_page_preview=True,
                             reply_to_message_id=self.msg_id)
        d = open('ban.mp4', 'rb')
        self.bot.sendVideoNote(self.chat_id, video_note=d)
        d.close()

    @admin
    @log
    def unban(self):
        list_ban_open = open('list_ban.txt', 'r')
        usersban = list_ban_open.read().split('\n')
        list_ban_open.close()

        if usersban != '':
            self.bot.unbanChatMember(self.chat_id, self.user_id)
            self.bot.sendMessage(chat_id=self.chat_id, 
                                parse_mode='HTML', 
                                text='<a href="https://telegram.me/{1}/">{0}</a> <b>unbanned by</b> <a href="https://telegram.me/{3}/">{2}</a>'.format(self.userresp,self.usernamerep, 
                                                                                                                            self.user, self.username), 
                                disable_web_page_preview=True,
                                reply_to_message_id=self.msg_id)
                                
            list_ban_open = open('list_ban.txt', 'w')
            usersban.remove(self.userresp)
            for i in usersban:
                list_ban_open.write(i+ '\n')
            list_ban_open.close()
        
    @admin	
    @log
    def warn(self, quanti):
        #add user's is
        if len(quanti) > 1:
            quanti[1] = int(quanti[1])
            with open('warn.txt', 'a') as warnlist: 
                for warn_qt in range(quanti[1]):
                    warnlist.write(self.user_id + '\n')
        else:
            with open('warn.txt', 'a') as warnlist: 
                warnlist.write(self.user_id + '\n')
        
        warnlist = open('warn.txt', 'r')
        file_read = warnlist.read().split('\n')
        warnlist.close()

        if file_read.count(self.user_id) >= 3:
            retur = self.ban(warn=True)
            return
        
        cont = file_read.count(self.user_id)
        self.bot.sendMessage(chat_id=self.chat_id, 
                             parse_mode='HTML', 
                             text='<a href="https://telegram.me/{1}/">{0}</a> <b>has been warned</b> (<i>{2}</i>/<b>3</b>)'.format(self.userresp, self.usernamerep,cont), 
                             reply_markup=self.keyboard_warn(), 
                             disable_web_page_preview=True,
                             reply_to_message_id=self.msg_id)
    @admin						 
    @log
    def unwarn(self, **keyword):
        
        list_warn_open = open('warn.txt', 'r')
        userswarn = list_warn_open.read().split('\n')
        list_warn_open.close()

        list_warn_open = open('warn.txt', 'w')
        if keyword.get('data', False):
                self.bot.answerCallbackQuery(callback_query_id=self.query_id, 
                                             text='Warn has been removed!',
                                             show_alert=False,
                                             cache_time=1)
                userswarn.remove(keyword['data'])

        else:
            userswarn.remove(self.user_id)

        for i in userswarn:
            list_warn_open.write(i+ '\n')
        list_warn_open.close()


    def keyboard_warn(self):
        return InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="Remove Warn", callback_data=str(self.user_id))]
                    ])
