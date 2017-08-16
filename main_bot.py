from telepot.loop import MessageLoop
import telepot
from handle import *
from punishment import punish
from greetings import greetings
from time import sleep
from sys import argv

def control(msg):

    try:
        main_inst = main(bot, msg)
        command_inst = command(bot, msg)
        greetings_inst = greetings(bot,msg)
        punish_inst = punish(bot, msg)
        if msg.get('data'):
            text = 'None'
            ctext = 'None'
            punish_inst = punish(bot, msg)
            punish_inst.unwarn(data=main_inst.query_data)

        else:
            text = msg['text'].split(' ')
            ctext = text[0].lower()

        if main_inst.chat_type == 'private':
            pass
        else:
            
            admin_commands = {
                          
                            '/ban':       punish_inst.ban,
                            '/unban':     punish_inst.unban,
                            '/warn':      punish_inst.warn,
                            'unwarn':     punish_inst.unwarn,
                            '/blacklist': command_inst.blacklist,
                            '/afklist':   command_inst.afklist,
                            '/clear':     command_inst.clearlists,
                            '/promote':   command_inst.promote_demote,
                            '/demote':    command_inst.promote_demote,
                            '/pin':       command_inst.pin,
                            '/unpin':     command_inst.pin
            }
        
            user_command = {

                            '/afk':       command_inst.afk,
                            '/back':      command_inst.back,
                            '/rules':     command_inst.rules,
                            '/admins':    command_inst.admin,
                            '@admin':     command_inst.repotadmin
            }


            if 'new_chat_member' in msg:
                greetings_inst.welcome()

            if admin_commands.get(ctext):
                if main_inst.get_admin_list():
                    if ctext.startswith('/warn'):
                        admin_commands[ctext](text)

                    elif ctext.startswith('/afklist', 0, 8):
                        admin_commands[ctext]()

                    elif ctext.startswith('/demote'):
                        admin_commands[ctext](admin=False)

                    else:
                        admin_commands[ctext]()
            elif user_command.get(ctext):
                user_command[ctext]()

  
            if ctext.lower().startswith('rt',0,2):
                if msg.get('reply_to_message', False):
                    if (text[0].lower() == 'rt' and len(text) == 1) or (text[0].lower() == 'rtzao' and len(text) == 1):
                        command_inst.rt()
                    else:
                        text = msg['text'].lower()
                        if ('rt' == text[0:2]) and (len(text[2:]) == 0) or ('rtzao' == text[0:2]) and (len(text[5:]) == 0): 
                            text = text.strip('rt')
                            command_inst.rt(text)
                        elif 'rtzao' == text[0:5]: 
                            text = text.strip('rtzao')
                            command_inst.rt(text)
                        
                        elif 'rt' == text[0:2]: 
                            text = text.strip('rtzao')
                            command_inst.rt(text)
              
    except:                                                                   
        pass
     

bot = telepot.Bot(argv[1])
print('Listening...')
MessageLoop(bot, control).run_as_thread()


while 1:
    sleep(100)
