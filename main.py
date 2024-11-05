import psutil
import json

def format_psutil_info():
    cpu_info = {
        'CPU Percent (%)': psutil.cpu_percent(interval=1),
        'CPU Count': psutil.cpu_count(),
        'CPU Frequency (MHz)': psutil.cpu_freq().current,
    }

    memory_info = {
        'Total Memory (GB)': round(psutil.virtual_memory().total / (1024 ** 3), 2),
        'Available Memory (GB)': round(psutil.virtual_memory().available / (1024 ** 3), 2),
        'Used Memory (GB)': round(psutil.virtual_memory().used / (1024 ** 3), 2),
        'Memory Usage (%)': psutil.virtual_memory().percent,
    }

    disk_info = {
        'Total Disk (GB)': round(psutil.disk_usage('/').total / (1024 ** 3), 2),
        'Used Disk (GB)': round(psutil.disk_usage('/').used / (1024 ** 3), 2),
        'Free Disk (GB)': round(psutil.disk_usage('/').free / (1024 ** 3), 2),
        'Disk Usage (%)': psutil.disk_usage('/').percent,
    }

    network_info = {}
    for interface, addrs in psutil.net_if_addrs().items():
        network_info[interface] = [{'Address': addr.address, 'Netmask': addr.netmask} for addr in addrs]

    info = {
        'CPU Information': cpu_info,
        'Memory Information': memory_info,
        'Disk Information': disk_info,
        'Network Information': network_info
    }

    return json.loads(json.dumps(info, indent=4, ensure_ascii=False))

formatted_info = format_psutil_info()
print(formatted_info)
