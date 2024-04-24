import datetime
import platform
import psutil
import logging

# Setting up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def get_disk_partitions():
    partitions = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "opts": part.opts,
                "total": usage.total / (1024**3), 
                "used": f"{usage.used / (1024**3):.2f} GB",
                "free": f"{usage.free / (1024**3):.2f} GB",
                "percent_used": f"{usage.percent}%"
            })
        except Exception as e:
            logger.error(f"Error getting disk usage for {part.mountpoint}: {str(e)}")
            continue
    
    sorted_partitions = sorted(partitions, key=lambda x: x['total'], reverse=True)
    for partition in sorted_partitions:
        partition['total'] = f"{partition['total']:.2f} GB"
        
    return sorted_partitions

def get_top_processes(limit=5):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            proc_info = proc.as_dict(attrs=['pid', 'name', 'username'])
            proc_info['cpu_percent'] = proc.cpu_percent(interval=None) 
            proc_info['cpu_overall'] =  f"{proc_info['cpu_percent']  / psutil.cpu_count():.2f}" 
            proc_info['memory_percent'] = f"{proc.memory_percent():.2f}"
            memory_info = proc.memory_info()
            proc_info['memory_usage'] = f"{memory_info.rss / (1024**2):.2f} MB",

            processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    top_processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:limit]
    return top_processes


def get_system_info():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    load_average = psutil.getloadavg() 
    cpu_percent = psutil.cpu_percent(interval=None, percpu=False) 
    
    system_info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": psutil.cpu_count(logical=True),
        "cpu_usage_percent": cpu_percent,
        "memory_total": f"{memory.total / (1024**3):.2f} GB",
        "memory_used": f"{memory.used / (1024**3):.2f} GB",
        "memory_free": f"{memory.available / (1024**3):.2f} GB",
        "disk_total": f"{disk.total / (1024**3):.2f} GB",
        "disk_used": f"{disk.used / (1024**3):.2f} GB",
        "disk_free": f"{disk.free / (1024**3):.2f} GB",
        "uptime": str(uptime),
        "load_average": {
            "1_min": f"{load_average[0]:.2f}",
            "5_min": f"{load_average[1]:.2f}",
            "15_min": f"{load_average[2]:.2f}"
        },
        "network_io": {
            "bytes_sent": f"{psutil.net_io_counters().bytes_sent / (1024**2):.2f} MB",
            "bytes_received": f"{psutil.net_io_counters().bytes_recv / (1024**2):.2f} MB"
        }
        
    }

    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery:
            system_info["battery"] = {
                "percent": f"{battery.percent}%",
                "power_plugged": battery.power_plugged
            }

    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            max_temp = max(core.current for core in temps['coretemp'])
            system_info["cpu_temperature"] = f"{max_temp}°C"
    
    if hasattr(psutil, "sensors_fans"):
        fans = psutil.sensors_fans()
        if "core" in fans:
            system_info["cpu_fan_speed"] = f"{fans['core'][0]} RPM"

    system_info['top_processes'] = get_top_processes()
    system_info['disk_partitions'] = get_disk_partitions()
    #system_info['top_command_output'] = get_top_command_output()
    return system_info



