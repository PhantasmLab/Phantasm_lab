from handle import main
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

class punish(main):
    
    def __init__(self, bot, msg):
        super().__init__(bot,msg)
        
        if self.msg['text'].split(' ')[0].lower() in ['/ban', '/unban', '/warn', '/unwarn']:
            if msg.get('data'):
                self.userresp = None
                self.user_id = None
                self.message_id = None
            else:
        
                self.userresp = self.msg['reply_to_message']['from']['first_name']
                self.usernamerep = self.msg['reply_to_message']['from']['username']
                self.user_id = self.msg['reply_to_message']['from']['id']
                self.message_id = self.msg['reply_to_message']['message_id']
                
                #add on list if user_reply is admin
                admin = self.bot.getChatAdministrators(self.chat_id)
                self.AdminID_list_reply = [adminID['user']['id'] for adminID in admin if self.user_id == adminID['user']['id']]

    def ban(self):
        #ban user
        if self.user_id in self.AdminID_list_reply:
            self.bot.sendMessage(chat_id=self.chat_id, 
                                parse_mode='HTML', 
                                text="<b>You can't ban a ADMIN!</b>",
                                reply_to_message_id=self.msg_id)
            return None
        self.bot.kickChatMember(self.chat_id,self.user_id)
        #add list
        with open('list_ban.txt', 'a') as list_ban:
            list_ban.write('<i>' + self.userresp + '<i>'+'\n')

        
        self.bot.sendMessage(chat_id=self.chat_id, 
                             parse_mode='Markdown', 
                             text='*sudo rm -rf* [{0}](https://telegram.me/{1}/)'.format(self.userresp,self.usernamerep), 
                             disable_web_page_preview=True,
                             reply_to_message_id=self.msg_id)
        d = open('ban.mp4', 'rb')
        self.bot.sendVideoNote(self.chat_id, video_note=d)
        d.close()

    def unban(self):
        list_ban_open = open('list_ban.txt', 'r')
        usersban = list_ban_open.read().split('\n')
        list_ban_open.close()
        print(usersban)
        if usersban != '':
            list_ban_open = open('list_ban.txt', 'w')
            usersban.remove(self.userresp)
            for i in usersban:
                list_ban_open.write(i+ '\n')
            list_ban_open.close()

            self.bot.unbanChatMember(self.chat_id, self.user_id)
            self.bot.sendMessage(chat_id=self.chat_id, 
                                parse_mode='Markdown', 
                                text='[{0}](https://telegram.me/{1}/) *unbanned by* [{2}](https://telegram.me/{3}/)'.format(self.userresp,self.usernamerep, self.user, self.username), 
                                disable_web_page_preview=True,
                                reply_to_message_id=self.msg_id)
        
        
        
    #funções warn requer ajustes

    def warn(self, quanti):
        #add user's is
        if len(quanti) > 1:
            quanti[1] = int(quanti[1])
            with open('warn.txt', 'a') as warnlist: 
                for warn_qt in range(quanti[1]):
                    warnlist.write(str(self.user_id) + '\n')
        else:
            with open('warn.txt', 'a') as warnlist: 
                warnlist.write(str(self.user_id) + '\n')
        
        warnlist = open('warn.txt', 'r')
        file_read = warnlist.read().split('\n')


        if file_read.count(str(self.user_id)) >= 3:
            self.bot.kickChatMember(self.chat_id,self.user_id)
            self.bot.sendMessage(chat_id=self.chat_id, 
                                 parse_mode='Markdown', 
                                 text='`[{0}](https://telegram.me/{1}/)` *banned:* reached the max number of warnings (`3/3`)'.format(self.userresp, self.usernamerep), 
                                 disable_web_page_preview=True,
                                 reply_to_message_id=self.msg_id)
            warnlist.close()
            return
        cont = file_read.count(str(self.user_id))
        self.bot.sendMessage(chat_id=self.chat_id, 
                             parse_mode='Markdown', 
                             text='[{0}](https://telegram.me/{1}/) *has been warned* (`{2}`/*3*)'.format(self.userresp, self.usernamerep,cont), 
                             reply_markup=self.keyboard_warn(), 
                             disable_web_page_preview=True,
                             reply_to_message_id=self.msg_id)


    def unwarn(self, **keyword):
        
        list_warn_open = open('warn.txt', 'r')
        userswarn = list_warn_open.read().split('\n')
        list_warn_open.close()

        list_warn_open = open('warn.txt', 'w')
        if keyword.get('data', False):
            if self.get_admin_list(query=True):
                userswarn.remove(keyword['data'])
        else:
            userswarn.remove(str(self.user_id))

        for i in userswarn:
            list_warn_open.write(i+ '\n')
        list_warn_open.close()


    def keyboard_warn(self):
        return InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="Remove Warn", callback_data=str(self.user_id))]
                    ])