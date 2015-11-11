import os

def isRPI():
    if not os.path.exists("/proc/cpuinfo"):
        return False
    with open("/proc/cpuinfo") as f:
        return f.read().index("BCM") != -1