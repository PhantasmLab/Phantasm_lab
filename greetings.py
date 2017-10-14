from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
import json
import requests

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
                            text='*Welcome(a) to the Group!*\n`User`: [{0}](https://telegram.me/{1}/);\n`id`: #id{2};\n`Channel`: [here](https://telegram.me/phantasm_lab).'.format(user_first_name, self.username, id_user),
                            disable_web_page_preview=True,
                            reply_markup=self.keyboard_welcome())
                

        v = open('giphy.mp4', 'rb')
        self.bot.sendVideoNote(self.chat_id, v, reply_to_message_id=self.msg_id)

        with open('bot.json', 'r') as file:
            json_file = json.load(file)
            key_id = 'id_msg'+str(self.chat_id)
            while 1:
                try:
                    json_file['welcome'][key_id]
                except KeyError:
                    json_file['welcome'][key_id] = []
                else:
                    break
        
        if json_file['welcome'][key_id]:
            for id in json_file['welcome'][key_id]:
                print(id)
                requests.post(
                    'https://api.telegram.org/bot428427082:AAHdv4elQ5XBKMmJMRqlqtKh4rgisIhhCgk/deleteMessage?chat_id={0}&message_id={1}'.format(self.chat_id, id)
                )

            json_file['welcome'][key_id].clear()
            json_file['welcome'][key_id].append(self.msg_id + 1)
            json_file['welcome'][key_id].append(self.msg_id + 2)

            with open('bot.json', 'w') as file:
                    json.dump(json_file, file, sort_keys=True, indent=4)
        else:
            json_file['welcome'][key_id].append(self.msg_id + 1)
            json_file['welcome'][key_id].append(self.msg_id + 2)
            
            with open('bot.json', 'w') as file:
                    json.dump(json_file, file, sort_keys=True, indent=4)


    def keyboard_welcome(self):
        
        return InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="Read the Rules", url='http://telegra.ph/Division-of-intelligence-08-05')]
                    ])
