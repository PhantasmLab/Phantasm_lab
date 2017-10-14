from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import json
import telepot
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

from bot_decorators import *
from handle import main

class punish(main):
    
    def __init__(self, bot, msg):
        super().__init__(bot,msg)
        
        if not(self.chat_type == 'channel'):
            if self.msg.get('text'):
                if self.msg['text'].split(' ')[0].lower() in ('/ban', '/unban', '/warn', '/unwarn'):
                    self.userresp   = self.msg['reply_to_message']['from']['first_name']               
                    self.user_id    = str(self.msg['reply_to_message']['from']['id'])
                    self.message_id = self.msg['reply_to_message']['message_id']
                    if msg['reply_to_message']['from'].get('username'):
                        self.usernamerep = self.msg['reply_to_message']['from']['username']
                    else:
                        self.usernamerep = 'No username'
    

        

    @admin			
    def ban(self, warn = False):     

        if int(self.user_id) in self.get_admin_list(user_reply = True):
            self.bot.sendMessage(chat_id   = self.chat_id, 
                                 parse_mode = 'HTML', 
                                 text       = "<b>You can't ban an ADMIN!</b>",
                                 reply_to_message_id = self.msg_id)
            return None

        self.bot.kickChatMember(self.chat_id, self.user_id)

        if warn:
            self.bot.sendMessage(chat_id    = self.chat_id, 
                                 parse_mode = 'HTML', 
                                 text       = '<a href="https://telegram.me/{1}/">{0}</a> <b>banned:</b> reached the max number of warnings (<b>3/3</b>)'.format(self.userresp, self.usernamerep), 
                                 disable_web_page_preview = True,
                                 reply_to_message_id      = self.message_id)

            self.dbexec.sql_update('ban', 1,self.user_id, self.userresp,self.usernamerep)
            return

        
        self.dbexec.sql_update('ban', 1,self.user_id,self.userresp, self.usernamerep)
        
        requests.post(
                        'https://api.telegram.org/bot428427082:AAHdv4elQ5XBKMmJMRqlqtKh4rgisIhhCgk/deleteMessage?chat_id={0}&message_id={1}'.format(
                            self.chat_id, 
                            self.message_id
                )
        )
        
        self.bot.sendMessage(chat_id    = self.chat_id, 
                             parse_mode = 'HTML', 
                             text       = '<a href="https://telegram.me/{1}/">{0}</a> <b>banned by</b> <a href="https://telegram.me/{2}/">{3}</a>'.format(self.userresp,self.usernamerep, self.username,self.user), 
                             disable_web_page_preview = True,
                             reply_to_message_id      = self.message_id)
        



    @admin
    def unban(self):
        if self.dbexec.is_banned(self.user_id):
            self.bot.unbanChatMember(self.chat_id, self.user_id)
            self.bot.sendMessage(chat_id    = self.chat_id, 
                                parse_mode = 'HTML', 
                                text       = '<a href="https://telegram.me/{1}/">{0}</a> <b>unbanned by</b> <a href="https://telegram.me/{3}/">{2}</a>'.format(
                                self.userresp,
                                self.usernamerep,
                                self.user, 
                                self.username), 
                                disable_web_page_preview = True,
                                reply_to_message_id      = self.msg_id)                         
            self.dbexec.sql_update('ban', 0,self.user_id, self.userresp, self.usernamerep)
            self.dbexec.sql_update('warn',0,self.user_id,self.usernamerep)


    @admin	
    def warn(self, quanti):
        if len(quanti) > 1:
                self.dbexec.sql_warn_and_unwarn(user_id=self.user_id,first_name=self.userresp,quanti=int(quanti[1]),username=self.usernamerep)
        else:
            self.dbexec.sql_warn_and_unwarn(self.user_id,self.userresp, self.usernamerep)
        
        if self.dbexec.get_warnings(self.user_id) >= 3:
            self.ban(warn=True)
            return
        
        cont = self.dbexec.get_warnings(self.user_id)
        
        
        self.bot.sendMessage(chat_id      = self.chat_id, 
                             parse_mode   = 'HTML', 
                             text         = '<a href="https://telegram.me/{1}/">{0}</a> <b>has been warned</b> ({2}/<b>3</b>)'.format(self.userresp, self.usernamerep,cont), 
                             reply_markup = self.keyboard_warn(), 
                             disable_web_page_preview = True,
                             reply_to_message_id = self.message_id)
        
        requests.post(
                        'https://api.telegram.org/bot428427082:AAHdv4elQ5XBKMmJMRqlqtKh4rgisIhhCgk/deleteMessage?chat_id={0}&message_id={1}'.format(
                            self.chat_id, 
                            self.message_id
                )
        )
        

    @admin						 
    def unwarn(self, **keyword):
        if keyword.get('data', False):
                self.bot.answerCallbackQuery(callback_query_id = self.query_id, 
                                             text       = 'Warn has been removed!',
                                             show_alert = False,
                                             cache_time = 1)

                self.dbexec.sql_warn_and_unwarn(int(keyword['data']), remove=True)
        else:
            self.dbexec.sql_warn_and_unwarn(self.user_id,self.userresp, remove=True)
            self.bot.sendMessage(self.chat_id,'warn has been removed!')
    

    @admin
    def banvote(self, username=None, temp=None, msg=None, tvotation=None):
        if msg == None:
            self.msg_id = self.msg_id + 1
            self.bot.sendMessage(self.chat_id, 'Creating Votation 0%')
            time.sleep(0.5)
            self.bot.editMessageText((self.chat_id, self.msg_id), 'Creating Votation 10%...')
            time.sleep(0.5)
            self.bot.editMessageText((self.chat_id, self.msg_id), 'Creating Votation 50%...')
            time.sleep(0.5)
            self.bot.editMessageText((self.chat_id, self.msg_id), 'Creating Votation 75%...')
            time.sleep(0.5)
            self.bot.editMessageText((self.chat_id, self.msg_id), 'Creating Votation 99%...')
            
            html = requests.get('https://telegram.me/{}'.format(username[1:]))
            soup = BeautifulSoup(html.text)
            name = soup.find('div', {'class': 'tgme_page_title'}).text

            with open('bot.json', 'r') as file:
                json_file = json.load(file)
                json_file['vote_ban']['temp'] = temp
                json_file['vote_ban']['id_msg'] = self.msg_id
                json_file['vote_ban']['time'] = datetime.now().strftime('%H:%M:%S').__str__()
                json_file['vote_ban']['agree'] = 0
                json_file['vote_ban']['time_votation'] = tvotation
                json_file['vote_ban']['disagree'] = 0
                json_file['vote_ban']['voted'] = []
                json_file['vote_ban']['name'] = name
                json_file['vote_ban']['admins'] = self.get_admin_list(user_reply=True)

                if self.dbexec.auth_if_user_exist("username = '{}'".format(username[1:]), username[1:]):
                    json_file['vote_ban']['id_user'] = self.dbexec.get_id('id',"'%s'"%username[1:])
                    json_file['vote_ban']['user_in_db'] = True
                else:
                    json_file['vote_ban']['id_user'] = None
                    json_file['vote_ban']['user_in_db'] = False

            with open('bot.json', 'w') as file:
                json.dump(json_file, file,sort_keys=True, indent=4)

            msg = '<b>{0}</b> has opened a votation to ban <b>{1}</b>.\n\n<b>TempBan</b>: {2}h\n[{3}] <b>Agree</b>\n[{4}] <b>Disagree</b>\n\n Votation will be closed in {5}min'.format(self.user, name, temp, 0,0,tvotation)
            self.bot.editMessageText(
                msg_identifier=(self.chat_id,self.msg_id),
                text=msg,
                parse_mode='HTML',
                reply_markup=self.keyboard_tempban()
            )
        else:
            if msg.get('vote_msg'):
                self.bot.editMessageText(
                    msg_identifier=(self.chat_id,msg['vote_msg'][0]),
                    text=msg['vote_msg'][1],
                    parse_mode='HTML',
                    reply_markup=self.keyboard_tempban()
                )
            elif msg.get('vote_query'):
                self.bot.answerCallbackQuery(callback_query_id = self.query_id, 
                                     text       = 'You have already voted.',
                                     show_alert = False,
                                     cache_time = 1
                )

            elif msg.get('vote_closed'):
                if msg['vote_closed'][2]['is_user_in_db']:
                    self.bot.editMessageText(
                        msg_identifier=(self.chat_id,msg['vote_closed'][0]),
                        text=msg['vote_closed'][1],
                        parse_mode='HTML',
                        reply_markup=self.keyboard_voteban(
                            msg['vote_closed'][2]['user'],
                            msg['vote_closed'][2]['user_id'],
                            msg['vote_closed'][2]['temp'])
                    )
                else:
                    self.bot.editMessageText(
                        msg_identifier=(self.chat_id,msg['vote_closed'][0]),
                        text=msg['vote_closed'][1],
                        parse_mode='HTML'
                    )
            
            elif msg.get('data'):
                data = msg['data'].split(':')
                if self.UserID in self.get_admin_list(user_reply=True):
                    try:
                        self.bot.kickChatMember(self.chat_id, int(data[0]), int(msg['data'][1]))
                        self.bot.answerCallbackQuery(callback_query_id = self.query_id, 
                                        text       = 'User banned.',
                                        show_alert = False,
                                        cache_time = 1
                    )
                    except telepot.exception.TelegramError:
                        self.bot.answerCallbackQuery(callback_query_id = self.query_id, 
                                        text       = "I can't ban an admin.",
                                        show_alert = False,
                                        cache_time = 1
                    )
                else:
                    self.bot.answerCallbackQuery(callback_query_id = self.query_id, 
                                         text       = 'You are not allowed to use this button!',
                                         show_alert = False,
                                         cache_time = 1
                    )
            
    def keyboard_voteban(self, user, id_user, temp):
        return InlineKeyboardMarkup(inline_keyboard    = [
                            [InlineKeyboardButton(text = "Press the button to ban {}".format(user), callback_data='{}:{}'.format(id_user,temp))]
                    ])

    def keyboard_warn(self):
        return InlineKeyboardMarkup(inline_keyboard    = [
                            [InlineKeyboardButton(text = "Remove Warn", callback_data=str(self.user_id))]
                    ])

    def keyboard_tempban(self):
        return InlineKeyboardMarkup(inline_keyboard    = [
                            [InlineKeyboardButton(text = "Agree", callback_data='agree'),
                            InlineKeyboardButton(text = "Disagree", callback_data='disagree')],
                    ]
                )