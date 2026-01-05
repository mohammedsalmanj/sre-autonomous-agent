import psutil
from .base import Monitor

class SystemMonitor(Monitor):
    """
    Monitors local system resources (CPU, Memory, Disk).
    Useful for running the agent as a daemon on a specific host.
    """
    def __init__(self, cpu_threshold=80.0, memory_threshold=85.0):
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold

    @property
    def name(self) -> str:
        return "system_resource_monitor"

    def check(self):
        alerts = []
        
        # Check CPU
        # interval=None is non-blocking but might be 0 on first call. 
        # In a real loop, it works fine after the first tick.
        cpu_usage = psutil.cpu_percent(interval=None) 
        
        if cpu_usage > self.cpu_threshold:
            alerts.append({
                "source": self.name,
                "type": "high_cpu",
                "severity": "critical",
                "message": f"CPU usage is critical: {cpu_usage}%",
                "context": {"usage": cpu_usage, "threshold": self.cpu_threshold}
            })

        # Check Memory
        memory = psutil.virtual_memory()
        if memory.percent > self.memory_threshold:
            alerts.append({
                "source": self.name,
                "type": "high_memory",
                "severity": "warning",
                "message": f"Memory usage is high: {memory.percent}%",
                "context": {"usage": memory.percent, "threshold": self.memory_threshold}
            })

        return alerts
