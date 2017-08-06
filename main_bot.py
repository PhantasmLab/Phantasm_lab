import telepot
from telepot.loop import MessageLoop
from handle import *
from punishment import punish
from greetings import greetings


def control(msg):
        
    global bot
    try:
        main_inst = main(bot, msg)
        command_inst = command(bot, msg)
        greetings_inst = greetings(bot,msg)
        if 'new_chat_member' in msg:
            greetings_inst.welcome()
        
        if msg.get('data'):
            text = 'None'
            ctext = 'None'
            punish_inst = punish(bot, msg)
            punish_inst.unwarn(data=main_inst.query_data)

        else:
            text = msg['text'].split(' ')
            ctext = text[0].lower()

        if ctext in ['/ban', '/unban', '/warn', '/unwarn']:
            punish_inst = punish(bot, msg)

        if main_inst.chat_type == 'private':
            pass
        else:
            if ctext.startswith('/ban'):
                if main_inst.get_admin_list():
                    punish_inst.ban()

            elif ctext.startswith('/unban'):
                if main_inst.get_admin_list():
                    punish_inst.unban()

            elif ctext.startswith('/clear'):
                if main_inst.get_admin_list():
                    return_resul = command_inst.clearlists(text)
                    bot.sendMessage(chat_id=main_inst.chat_id, parse_mode='HTML', text=return_resul)

            elif ctext.startswith('/afklist', 0, 8):
                if main_inst.get_admin_list():
                    command_inst.afklist()

            elif ctext.startswith('/blacklist'):
                if main_inst.get_admin_list():
                    command_inst.blacklist()

            elif ctext.startswith('/warn'):
                if main_inst.get_admin_list():
                    punish_inst.warn(text)

            elif ctext.startswith('/unwarn'):
                if main_inst.get_admin_list():
                    punish_inst.unwarn()
                    

            elif ctext.startswith('/rules'):
                command_inst.rules()

            elif ctext.startswith('/back'):
                command_inst.back()

            elif ctext == '/afk':
                command_inst.afk(text)
            
            elif ctext == '/pin':
                command_inst.pin()
            
            elif ctext.startswith('/unpin'):
                command_inst.unpin()
            
            elif ctext.startswith('/promote'):
                if main_inst.get_admin_list():
                    command_inst.promote_demote()
                    bot.sendMessage(chat_id=main_inst.chat_id, text='{0} agora e admin.'.format(command_inst.adminuser))
                    
            elif ctext.startswith('/demote'):
                if main_inst.get_admin_list():
                    command_inst.promote_demote(admin=False)
                    bot.sendMessage(chat_id=main_inst.chat_id, text='{0} não e mais admin.'.format(command_inst.adminuser))
            
            elif ctext.startswith('/link'):
                if main_inst.get_admin_list():
                    bot.sendMessage(chat_id=main_inst.chat_id,parse_mode='Markdown', text='[Division of intelligence | #PL ]({})'.format(command_inst.link()), disable_web_page_preview=True)
                
            elif ctext.lower().startswith('rt',0,2):
                if msg.get('reply_to_message', False):
                    if (text[0].lower() == 'rt' and len(text) == 1) or (text[0].lower() == 'rtzao' and len(text) == 1):
                        command_inst.rt()
                    else:
                        text = msg['text'].lower()
                        if ('rt' == text[0:2]) and (len(text[2:]) == 0): text = text.strip('rt'); command_inst.rt(text)
                        elif 'rtzao' == text[0:5]: text = text.strip('rtzao'); command_inst.rt(text)

        
        
        
      
    except:                                                                   
        pass

        


bot = telepot.Bot('token')
print('Listening...')
MessageLoop(bot,control).run_as_thread()

while 1:
    pass
