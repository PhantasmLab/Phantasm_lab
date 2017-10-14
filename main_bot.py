import requests
import telepot
from sys import argv
from time import sleep
from telepot.loop import MessageLoop


from bot_decorators import check
from greetings import greetings
from handle import command, main
from punishment import punish

token = argv[1]

@check
def control(msg):
    #try:
        main_inst      = main(bot, msg)
        command_inst   = command(bot, msg)
        greetings_inst = greetings(bot,msg)
        punish_inst    = punish(bot, msg)
        
        if msg.get('data') and not(msg.get('permission') == False):
            text  = ''
            ctext = ''
            if msg['data'].isdigit():
                punish_inst.unwarn(data=main_inst.query_data)
            elif isinstance(msg['data'], str) and not(msg['data'] in ('agree', 'disagree')):
                punish_inst.banvote(msg=msg)

        if msg.get('text'):
            text  = msg['text'].split(' ')
            ctext = text[0].lower()
        else:
            ctext = ''
        if not (main_inst.chat_type == 'private'):
    
            admin_commands = {
                    '/ban':       punish_inst.ban,
                    '/unban':     punish_inst.unban,
                    '/warn':      punish_inst.warn,
                    '/unwarn':    punish_inst.unwarn,
                    '/blacklist': command_inst.blacklist,
                    '/afklist':   command_inst.afklist,
                    '/clear':     command_inst.clearlists,
                    '/promote':   command_inst.promote_demote,
                    '/demote':    command_inst.promote_demote,
                    '/pin':       command_inst.pin,
                    '/unpin':     command_inst.unpin,
                    '/uptime':    command_inst.uptime,
                    '/voteban':   punish_inst.banvote,
                    '/test': command_inst.kitploit_articles
            }
            
            user_command = {
                    '/afk':       command_inst.afk,
                    '/back':      command_inst.back,
                    '/rules':     command_inst.rules,
                    '/admins':    command_inst.admins,
                    '/help':      command_inst.help
            }
            

            if msg.get('new_chat_participant'):
                greetings_inst.welcome()
                main_inst.dbexec.insert_if_not_exists(
                    first_name=msg['new_chat_member']['first_name'],
                    user_id=msg['new_chat_member']['id'],
                    username = msg['new_chat_member']['username']
                )
                
                main_inst.dbexec.sql_update(
                    'ban','DEFAULT',
                    msg['new_chat_member']['id'],
                    msg['new_chat_member']['first_name']
                )

            elif user_command.get(ctext):
                user_command[ctext]()

            elif admin_commands.get(ctext):
                
                if ctext.startswith('/warn'):
                    admin_commands[ctext](text)
                elif ctext.startswith('/afklist', 0, 8):
                    admin_commands[ctext]()

                elif ctext.startswith('/voteban'):
                    if len(text) == 4:
                        if text[1].startswith('@') and text[2].isdigit() and text[3].isdigit():
                            punish_inst.banvote(username=text[1], temp=text[2], tvotation=text[3])
                    else:
                        bot.sendMessage(chat_id=main_inst.chat_id,parse_mode='Markdown', text='*Invalid Command.*\n*Command:* `/voteban [@username] [TimeBan] [TimeVotation]`')
                elif ctext.startswith('/demote'):
                    admin_commands[ctext](admin=False)
                else:
                    admin_commands[ctext]()
                        

            elif ctext.startswith('rt',0,2):
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
            
            elif msg.get('back'):
                bot.sendMessage(main_inst.chat_id, msg['back'])

            elif msg.get('ban'):
                bot.kickChatMember(main_inst.chat_id, msg['ban']['userid'])
                bot.sendMessage(
                    main_inst.chat_id,
                    parse_mode='HTML', 
                    text='<a href="https://telegram.me/{0}/">{1}</a> <b>has been banned for flood</b>'.format(
                        msg['ban']['username'],
                        msg['ban']['first_name']),
                    disable_web_page_preview=True,
                    reply_to_message_id=msg['ban']['msgid'][0])
                for id in msg['ban']['msgid']:
                    requests.post(
                        'https://api.telegram.org/bot428427082:AAHdv4elQ5XBKMmJMRqlqtKh4rgisIhhCgk/deleteMessage?chat_id={0}&message_id={1}'.format(main_inst.chat_id, id))
                main_inst.dbexec.sql_update('ban',1)

            elif msg.get('vote_msg') or msg.get('vote_query') or msg.get('vote_closed'):
                punish_inst.banvote(msg=msg)
            
            elif msg.get('permission'):
                main_inst.get_admin_list(query=True)
            
            elif msg.get('article'):
                command_inst.kitploit_articles()
            
                
    #except:                                                                   
    #    pass
   

bot = telepot.Bot(token)

if __name__ == '__main__':
    print('Listening...')
    MessageLoop(bot, control).run_as_thread()

    while 1:
        sleep(100)