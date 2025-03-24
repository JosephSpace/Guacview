import psutil
import time
from flask import jsonify

def get_system_stats():
    # CPU kullanımı
    cpu_percent = psutil.cpu_percent(interval=0.1, percpu=True)
    cpu_avg = sum(cpu_percent) / len(cpu_percent)
    
    # Bellek kullanımı
    memory = psutil.virtual_memory()
    memory_used = memory.used / (1024 * 1024 * 1024)  # GB cinsinden
    memory_total = memory.total / (1024 * 1024 * 1024)  # GB cinsinden
    memory_percent = memory.percent
    
    # Disk kullanımı
    disk = psutil.disk_usage('/')
    disk_used = disk.used / (1024 * 1024 * 1024)  # GB cinsinden
    disk_total = disk.total / (1024 * 1024 * 1024)  # GB cinsinden
    disk_percent = disk.percent
    
    # Ağ kullanımı
    net_io_counters = psutil.net_io_counters()
    bytes_sent = net_io_counters.bytes_sent / (1024 * 1024)  # MB cinsinden
    bytes_recv = net_io_counters.bytes_recv / (1024 * 1024)  # MB cinsinden
    
    # Zaman damgası
    timestamp = int(time.time() * 1000)  # milisaniye cinsinden
    
    return {
        'timestamp': timestamp,
        'cpu': {
            'percent': cpu_percent,
            'average': cpu_avg
        },
        'memory': {
            'used': round(memory_used, 2),
            'total': round(memory_total, 2),
            'percent': memory_percent
        },
        'disk': {
            'used': round(disk_used, 2),
            'total': round(disk_total, 2),
            'percent': disk_percent
        },
        'network': {
            'sent': round(bytes_sent, 2),
            'received': round(bytes_recv, 2)
        }
    }