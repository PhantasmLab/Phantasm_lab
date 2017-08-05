import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from handle import *
from punishment import punish



def control(msg):
    
    global bot

    try:
        main_inst = main(bot, msg)
        command_inst = command(bot, msg)

        if msg.get('data'):
            text = 'None'
            ctext = 'None'
            punish_inst = punish(bot, msg)
            punish_inst.unwarn(data=msg['data'])

        else:
            text = msg['text'].split(' ')
            ctext = text[0]

        if ctext in ['/ban', '/unban', '/warn', '/unwarn']:
            punish_inst = punish(bot, msg)


        if ctext.startswith('/ban'):
            if main_inst.get_admin_list():
                punish_inst.ban()

        if ctext.startswith('/unban'):
            if main_inst.get_admin_list():
                punish_inst.unban()

        if ctext.startswith('/clear'):
            return_resul = command_inst.clearlists(text)
            bot.sendMessage(chat_id=main_inst.chat_id, parse_mode='HTML', text=return_resul)

        if ctext.startswith('/afklist', 0, 8):
            if main_inst.get_admin_list():
                command_inst.afklist()

        if ctext.startswith('/blacklist'):
            if main_inst.get_admin_list():
                command_inst.blacklist()

        if ctext.startswith('/warn'):
            if main_inst.get_admin_list():
                punish_inst.warn(text)

        if ctext.startswith('/unwarn'):
            if main_inst.get_admin_list():
                punish_inst.unwarn()
                

        if ctext.startswith('/rules'):
            command_inst.rules()

        if ctext.startswith('/back'):
            command_inst.back()

        if ctext == '/afk':
            print('aqui')
            command_inst.afk(text)
        
        if ctext == '/pin':
            command_inst.pin()
        
        if ctext.startswith('/unpin'):
            command_inst.unpin()
    except:
        pass

        


bot = telepot.Bot('token')
print('Listening...')
bot.message_loop(control)


while 1:
    pass