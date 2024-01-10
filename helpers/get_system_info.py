import subprocess


async def get_system_info():
    try:
        output = subprocess.check_output('systeminfo', shell=True)
        return output.decode('cp866')
    except Exception as e:
        return f"Ошибка получения системной информации: {e}"
