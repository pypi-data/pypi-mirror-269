import os.path

import psutil
from gpustat.core import GPUStatCollection

if __name__ == "__main__":
    psutil.cpu_percent()
    psutil.virtual_memory()
    psutil.disk_usage(os.path.expanduser("~"))

    gpu_stats = GPUStatCollection.new_query()
