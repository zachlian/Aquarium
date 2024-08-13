# hardware_monitor.py
import psutil
import GPUtil

class HardwareMonitor:
    @staticmethod
    def get_cpu_usage():
        return psutil.cpu_percent()

    @staticmethod
    def get_memory_usage():
        return psutil.virtual_memory().percent

    @staticmethod
    def get_gpu_usage():
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0].load * 100
            return None
        except:
            return None

# monitor = HardwareMonitor()
# cpu = monitor.get_cpu_usage()
# memory = monitor.get_memory_usage()
# gpu = monitor.get_gpu_usage()
# print(f'CPU: {cpu}%')
# print(f'Memory: {memory}%')
# print(f'GPU: {gpu}%')