from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from subprocess import check_output
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import re
import json
import telepot

from bot_decorators import *
from sql import *

class main:

    def __init__(self, bot, msg):

        self.bot    = bot
        self.msg    = msg

        if msg.get('data'):
            self.chat_id    = msg['message']['chat']['id']
            self.chat_type  = msg['message']['chat']['type']
            self.query_id, self.from_id, self.query_data = telepot.glance(msg, flavor='callback_query')
                
        else:
            self.msg_id     = msg['message_id']	
            self.content_type, self.chat_type, self.chat_id = telepot.glance(msg)
            
        if self.chat_type == 'channel':
            self.chat_id = msg['chat']['id']
            with open('bot.json') as file:
                self.json_file = json.load(file)
                if self.chat_id not in self.json_file['article']['send_for']:
                    self.json_file['article']['send_for'].append(self.chat_id)
            with open('bot.json', 'w') as file:
                json.dump(self.json_file,file, sort_keys=True, indent=4)
        else:
                     
            if msg['from'].get('username'):
                self.username = msg['from']['username']
            else:
                self.username = 'No Username'

            self.UserID = msg['from']['id']
            self.user   = msg['from']['first_name']

            with open('bot.json') as file:
                self.json_file = json.load(file)
                if self.chat_id not in self.json_file['article']['send_for']:
                    self.json_file['article']['send_for'].append(self.chat_id)
            with open('bot.json', 'w') as file:
                json.dump(self.json_file,file, sort_keys=True, indent=4)

            self.dbexec = sql_data(
                sql_connection(host='localhost',
                            user='root',
                            password='pass',
                            db='phantasm_lab'), 
                self.chat_id,
                self.UserID,
                self.user,
                self.username
            )
        
    
    def get_admin_list(self, query=False, user_reply=False):
        admin = self.bot.getChatAdministrators(self.chat_id)
        AdminID_list = [adminID['user']['id'] for adminID in admin]

        if user_reply:
            return AdminID_list

        if self.UserID in AdminID_list:
            return True
        
        if query != False:
            if self.UserID in AdminID_list:
                return True

            self.bot.answerCallbackQuery(callback_query_id = self.query_id, 
                                         text       = 'You are not allowed to use this button!',
                                         show_alert = False,
                                         cache_time = 1
                    )
            

        self.bot.sendMessage(chat_id    = self.chat_id,
                             parse_mode = 'HTML', 
                             text       = '<b>YOU DO NOT HAVE THE PERMISSION TO USE THIS COMMAND!</b>'
            )
    
    def get_creator(self):
        creator = self.bot.getChatAdministrators(self.chat_id)
        creator_id = [c_id['user']['id'] for c_id in creator if c_id['status'] == 'creator']
        
        if self.UserID in creator_id:
            return True
        self.bot.sendMessage(chat_id    = self.chat_id,
                             parse_mode = 'HTML', 
                             text       = '<b>ONLY THE CREATOR CAN USE THIS COMMAND!</b>', 
                             reply_to_message_id = self.msg_id)


class command(main):
    
    def afk(self):
        motivo = self.msg['text'][5:]
        if self.dbexec.is_user_afk_or_back('afk'):
            if len(motivo) == 0:
                msgafk = '<b>User:</b> <a href="https://telegram.me/{1}/">{0}</a> is now afk!<b>\nReason</b>: Not specified.'.format(self.user, self.username)
                #data.afk(self.user)
                self.dbexec.sql_afk_back_update('afk')

            else:
                msgafk = '<b>User:</b> <a href="https://telegram.me/{1}/">{0}</a> <b>is now afk!\nReason</b>: {2}'.format(self.user,self.username,motivo)
                #data.afk(self.user)
                self.dbexec.sql_afk_back_update('afk')
            self.bot.sendMessage(chat_id    = self.chat_id,
                                 parse_mode = 'HTML', 
                                 text       = msgafk, 
                                 disable_web_page_preview = True, 
                                 reply_to_message_id      = self.msg_id)


    @admin
    def afklist(self): 
        resul = self.dbexec.get_lists('afk')
        if resul == '':
            self.bot.sendMessage(chat_id    = self.chat_id,
                                 parse_mode = 'HTML', 
                                 text       = '<b>No Users in the list!</b>',
                                 reply_to_message_id = self.msg_id)
            return       
        self.bot.sendMessage(chat_id = self.chat_id,text = resul, reply_to_message_id = self.msg_id)


    def back(self):
        if self.dbexec.is_user_afk_or_back('back'):
            self.dbexec.sql_afk_back_update('back')
            self.bot.sendMessage(chat_id    = self.chat_id, 
                                parse_mode = 'HTML', 
                                text       = '<b>User</b> <a href="https://telegram.me/{1}/">{0}</a> <b>is back!</b>'.format(self.user, self.username), 
                                disable_web_page_preview = True,
                                reply_to_message_id      = self.msg_id)


    @admin
    def clearlists(self):
        clear = self.msg['text'].split(' ')
        resp  = self.dbexec.clear_values(clear)
        self.bot.sendMessage(chat_id    = self.chat_id, 
                             parse_mode = 'HTML', 
                             text       = resp,
                             reply_to_message_id = self.msg_id)


    @admin
    def blacklist(self):
        resul = self.dbexec.get_lists('ban')
        if  resul == '':
            self.bot.sendMessage(parse_mode = 'HTML',
                                 chat_id    = self.chat_id,
                                 text       = '<b>No Users in the list!</b>',
                                 reply_to_message_id = self.msg_id)
            return
        self.bot.sendMessage(parse_mode = 'Markdown',
                             chat_id    = self.chat_id,
                             text       = resul,
                             reply_to_message_id = self.msg_id)


    def rules(self):		
        self.bot.sendMessage(parse_mode = 'HTML',
                             chat_id    = self.chat_id,
                             text       = '<a href="http://telegra.ph/Division-of-intelligence-08-05">rules</a>',
                             reply_to_message_id = self.msg_id)


    @admin
    def pin(self):
        message_id = self.msg['reply_to_message']['message_id']
        self.bot.pinChatMessage(chat_id = self.chat_id, message_id = message_id)


    @admin
    def unpin(self):
        self.bot.unpinChatMessage(chat_id=self.chat_id)
    

    @admin
    def promote_demote(self, admin = True):
        if self.get_creator():
            adminuser = self.msg['reply_to_message']['from']['first_name']
            self.bot.promoteChatMember(chat_id             = self.chat_id, user_id      = self.msg['reply_to_message']['from']['id'],
                                       can_change_info     = admin, can_post_messages   = None, 
                                       can_edit_messages   = None, can_delete_messages  = admin, 
                                       can_invite_users    = admin, can_pin_messages    = admin, 
                                       can_promote_members = None, can_restrict_members = admin)

            if admin:
                self.bot.sendMessage(chat_id = self.chat_id, 
                                    text     = '{0} has become an admin.'.format(adminuser),
                                    reply_to_message_id = self.msg_id)
            else:
                self.bot.sendMessage(chat_id = self.chat_id, 
                                    text     = '{0} is not an admin anymore.'.format(adminuser),
                                    reply_to_message_id = self.msg_id)


    def rt(self, text=None):
        idmsg    = self.msg['reply_to_message']['message_id']
        userresp = self.msg['reply_to_message']['from']['first_name']
        username = self.msg['reply_to_message']['from']['username']

        if self.msg['reply_to_message'].get('text'):
            message  = self.msg['reply_to_message']['text']

            if text is None:
                self.bot.sendMessage(parse_mode = 'HTML',
                                 chat_id    = self.chat_id,
                                 text       = '🔊 <a href="https://telegram.me/{1}/">{0}</a>' 
                                 ' agree with <a href="https://telegram.me/{3}/">{2}</a>!\n\n💬: <b>{4}</b>'.format(
                                 self.user,
                                 self.username,
                                 userresp,
                                 username,
                                 message), 
                                 reply_to_message_id      = idmsg, 
                                 disable_web_page_preview = True)

            else:
                self.bot.sendMessage(parse_mode = 'HTML',
                                    chat_id    = self.chat_id,
                                    text       = '🔊 <a href="https://telegram.me/{1}/">{0}</a> agree withh '   
                                    '<a href="https://telegram.me/{3}/">{2}</a>!\n\n💬: <b>{4}</b>\n\n🗯: {5}'.format(
                                    self.user,
                                    self.username,
                                    userresp,
                                    username,
                                    message,
                                    text), 
                                    reply_to_message_id      = idmsg, 
                                    disable_web_page_preview = True)


        else:        
            if text is None:
                self.bot.sendMessage(parse_mode = 'HTML',
                                    chat_id    = self.chat_id,
                                    text       = '🔊 <a href="https://telegram.me/{1}/">{0}</a>' 
                                    ' agree with <a href="https://telegram.me/{3}/">{2}</a>!'.format(
                                    self.user,
                                    self.username,
                                    userresp,
                                    username), 
                                    reply_to_message_id      = idmsg, 
                                    disable_web_page_preview = True)


    

    def admins(self):
        admin  = ['├ '+adminuser['user']['first_name'] + '\n' for adminuser in self.bot.getChatAdministrators(self.chat_id)]           
        admins = ''.join(admin[:-1])
        msg    = '👤 <b>Creator</b>:\n└{0}\nAdmins:\n{1}'.format(admin[-1][1:], admins)
        
        self.bot.sendMessage(chat_id    = self.chat_id,
                             parse_mode = 'HTML',
                             text       = msg,
                             reply_to_message_id = self.msg_id)
    

   
    def help(self):
      self.bot.sendMessage(chat_id=self.chat_id,parse_mode='Markdown',text="The only commands i accept are the follows:\n"
      "`admins, back, unban, blacklist, promote, clear, demote, ban,voteban,"
      " warn, uptime,unwarn, afklist, unpin, pin, afk, rules,` and `@admin`."
     )  


    @admin
    def uptime(self):
        self.bot.sendMessage(self.chat_id, check_output('uptime -p',shell=True))

    
    def kitploit_articles(self):
        browser = webdriver.PhantomJS()
        browser.set_page_load_timeout(20)
        while 1:
            try:
                browser.get('http://www.kitploit.com')
            except TimeoutException:
                continue
            else:
                break

        Soup = BeautifulSoup(browser.page_source)
        source = str(Soup.find('div', {'class' : 'post'}))
        title = Soup.find('h2', {'class': 'post-title'}).text
        url = Soup.find('h2', {'class': 'post-title'}).find('a')['href']
        thumb = Soup.find('div', {'class':'thumb'}).find('a')
        url_img = re.findall(r'\(.*?\)',thumb.attrs['style'])[0][1:-1] #[1:-1] remove parentheses

        with open('kitploit_article.txt', 'r') as file:
            if not(file.read() == source):
                if not(url_img[-3:] == 'gif'):
                    for chat in self.json_file['article']['send_for']:
                        self.bot.sendPhoto(
                            chat_id=chat, 
                            photo=url_img, 
                            caption='{0}'.format(title),
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text="Read More", url=url)]
                            ])
                        )
                else:
                   for chat in self.json_file['article']['send_for']:
                        self.bot.sendVideo(
                            chat_id=chat, 
                            video=url_img, 
                            caption='{0}'.format(title),
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text="Read More", url=url)]
                            ])
                        ) 

                with open('kitploit_article.txt', 'w') as file:
                    file.write(source)