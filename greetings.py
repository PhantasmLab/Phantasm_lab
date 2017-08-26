from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

from handle import main


class greetings(main):

    def welcome(self):
        if self.msg['new_chat_member'].get('username'):
            self.username = self.msg['new_chat_member']['username']
        else:
            self.username = 'No Username'
        user_first_name = self.msg['new_chat_member']['first_name']
        id_user = self.msg['new_chat_member']['id']

        self.bot.sendMessage(chat_id=self.chat_id, 
                            parse_mode='Markdown', 
                            text='*Welcome(a) to the Group!*\n`User`: [{0}](https://telegram.me/{1}/);\n`id`: #id{2};\n`Channel`: [here](https://telegram.me/link_here).'.format(user_first_name, self.username, id_user),
                            disable_web_page_preview=True,
                            reply_markup=self.keyboard_welcome())
    
    def keyboard_welcome(self):
        
        return InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="Read the Rules", url='link')]
                    ])
