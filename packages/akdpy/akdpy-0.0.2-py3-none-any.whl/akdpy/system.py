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
    print("Getting system info...")
    print(get_disk_partitions())
    print(get_top_processes())


