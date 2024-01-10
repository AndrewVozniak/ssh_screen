import asyncio
import threading
import os
import inspect
import argparse

from config import server_config
from controllers.sshController import sshController
from controllers import botController

parser = argparse.ArgumentParser(description='SSH Client')
parser.add_argument('--username', help='SSH username', required=True)
parser.add_argument('--password', help='SSH password', required=True)
parser.add_argument('--server_ip', help='SSH server IP', required=True)
parser.add_argument('--timeout', help='SSH timeout', required=False, default=10)
parser.add_argument('--token', help='Telegram bot token', required=True)
parser.add_argument('--secret_phrase', help='Telegram bot secret phrase', required=True)

args = parser.parse_args()

server_config['username'] = args.username
server_config['password'] = args.password
server_config['server_ip'] = args.server_ip

botController.bot_config['token'] = args.token
botController.bot_config['secret_phrase'] = args.secret_phrase


async def ssh():
    controller = sshController(
        username=server_config['username'],
        password=server_config['password'],
        server_ip=server_config['server_ip'],
        main_file_path=os.path.abspath(inspect.getfile(inspect.currentframe()))
    )
    await controller.start()


async def bot():
    botController.start_bot()


def run_bot():
    asyncio.run(bot())


def run_ssh():
    asyncio.run(ssh())


bot_thread = threading.Thread(target=run_bot)
bot_thread.start()

ssh_thread = threading.Thread(target=run_ssh)
ssh_thread.start()
