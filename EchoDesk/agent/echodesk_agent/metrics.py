"""System metrics collection"""

import psutil
from datetime import datetime


class MetricsCollector:
    """Collects system metrics"""

    def collect_all(self) -> dict:
        """Collect all system metrics"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "cpu": self.collect_cpu(),
            "memory": self.collect_memory(),
            "disk": self.collect_disk(),
            "network": self.collect_network(),
        }

    def collect_cpu(self) -> dict:
        """Collect CPU metrics"""
        return {
            "percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count(),
            "count_logical": psutil.cpu_count(logical=True),
        }

    def collect_memory(self) -> dict:
        """Collect memory metrics"""
        mem = psutil.virtual_memory()
        return {
            "total_gb": round(mem.total / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
            "used_gb": round(mem.used / (1024**3), 2),
            "percent": mem.percent,
        }

    def collect_disk(self) -> dict:
        """Collect disk metrics"""
        disk = psutil.disk_usage("/")
        return {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percent": disk.percent,
        }

    def collect_network(self) -> dict:
        """Collect network metrics"""
        net = psutil.net_io_counters()
        return {
            "bytes_sent": net.bytes_sent,
            "bytes_recv": net.bytes_recv,
            "packets_sent": net.packets_sent,
            "packets_recv": net.packets_recv,
        }
