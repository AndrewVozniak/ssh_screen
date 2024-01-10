import subprocess


def get_used_ports(range_start=5000, range_end=65000):
    """Возвращает список используемых портов в заданном диапазоне."""
    command = 'netstat -ano'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    lines = result.stdout.splitlines()

    used_ports = set()
    for line in lines:
        parts = line.split()
        if len(parts) >= 4 and parts[1].startswith('0.0.0.0:'):
            port = int(parts[1].split(':')[1])
            if range_start <= port <= range_end:
                used_ports.add(port)

    return used_ports
