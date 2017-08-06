from handle import main
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

class greetings(main):

    def welcome(self):
        
        user_first_name = self.msg['new_chat_member']['first_name']
        username = self.msg['new_chat_member']['username']
        id_user = self.msg['new_chat_member']['id']

        self.bot.sendMessage(chat_id=self.chat_id, 
                            parse_mode='Markdown', 
                            text='*Bem Vindo(a) ao Grupo*, [{0}](https://telegram.me/{1}/).\n*id*: #{2};\n*Canal*: [here](https://telegram.me/phantasm_lab)'.format(user_first_name, username, id_user),
                            disable_web_page_preview=True,
                            reply_markup=self.keyboard_welcome())
    
    def keyboard_welcome(self):
        
        return InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="Leia as Regras", url='link')]
                    ])
