import configparser
import os
import time

import telepot
import yaml
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from zabbix_api import ZabbixAPI

basedir = os.path.abspath(os.path.dirname(""))

cfg = configparser.ConfigParser()
cfg.read(os.path.join(basedir, 'config.ini'), encoding='utf-8')

key = cfg['TELEGRAM']['key']
user_id = cfg['TELEGRAM']['user_id']
group_id = cfg['TELEGRAM']['group_id']
server = cfg['ZABBIX']['server']
username = cfg['ZABBIX']['username']
password = cfg['ZABBIX']['password']

zapi = ZabbixAPI(server=server)
zapi.login(username, password)

bot = telepot.Bot(key)


def status_link():
    with open('interfaces.yml') as iface:
        data = yaml.load(iface, Loader=yaml.FullLoader)

    load = data['servers']
    servers = load.keys()

    for server in servers:
        for interfaces in load[server]:
            filter_down = zapi.item.get({
                'output': 'extend',
                'filter': {
                    'host': server
                },
                'search': {
                    'key_': load[server][interfaces][1]
                }
            })

            filter_up = zapi.item.get({
                'outpurt': 'extend',
                'filter': {
                    'host': server
                },
                'search': {
                    'key_': load[server][interfaces][2]
                }
            })

            # Converte para inteiro
            down = int(filter_down[0]['lastvalue'])
            up = int(filter_up[0]['lastvalue'])

            # Converte download para Mbps ou Gbps
            if down >= 1000000000:
                down = ("%.2f Gbps" % (down / 1000000000))
            else:
                down = ("%d Mbps" % (down / 1000000))

            # Converte upload para Mbps ou Gbps
            if up >= 1000000000:
                up = ("%.2f Gbps" % (up / 1000000000))
            else:
                up = ("%d Mbps" % (up / 1000000))

            send = ('%s - %s\nInput: %s\nOutput: %s' %
                    (server, load[server][interfaces][0], down, up))

            bot.sendMessage(user_id, send)


def on_chat_message(msg):
    cotent_type, chat_type, chat_id = telepot.glance(msg)

    msg = msg['text']

    if '/menu' in msg:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='Link', callback_data='link'),
            InlineKeyboardButton(text='Status', callback_data='status')
        ]])

        bot.sendMessage(chat_id, 'Menu', reply_markup=keyboard)


def on_callback_query(msg):
    query_id, form_id, query_data = telepot.glance(msg,
                                                   flavor='callback_query')

    if query_data == 'link':
        status_link()
    if query_data == 'status':
        bot.sendMessage(group_id, 'Em desenvolvimento')


def start_app():
    print('Listening...')
    bot.message_loop({
        'chat': on_chat_message,
        'callback_query': on_callback_query
    })

    while 1:
        time.sleep(3)
