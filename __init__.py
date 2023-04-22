import os
import platform
import socket
import psutil
import datetime
import time
import subprocess
import netifaces
import uuid
import getpass
import wmi
import shutil
import math
import ctypes
import locale
import tempfile
import ctypes.wintypes
import winreg
import platform

def get_cpu_temperature():
    """Get the current CPU temperature in degrees Celsius."""
    if platform.system() == "Windows":
        result = subprocess.run(["WMIC", "CPU", "GET", "Temperature"], capture_output=True)
        temperature_str = result.stdout.decode().split("\n")[1].strip()
        if temperature_str:
            temperature = int(temperature_str) / 10.0
            return temperature
    else:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temperature_str = f.read().strip()
            if temperature_str:
                temperature = int(temperature_str) / 1000.0
                return temperature

def get_gpu_temperature():
    """Get the current GPU temperature in degrees Celsius."""
    if platform.system() == "Windows":
        # Use WMI to get the current GPU temperature on Windows
        wmi_obj = wmi.WMI(namespace="root\\WMI")
        temperature = None
        for gpu in wmi_obj.query("SELECT * FROM MSAcpi_ThermalZoneTemperature"):
            if gpu.CurrentTemperature != -1 and "gpu" in gpu.InstanceName.lower():
                temperature = gpu.CurrentTemperature / 10.0 - 273.15
                break
        return temperature
    else:
        # Assume Nvidia GPU and use nvidia-smi to get the current GPU temperature on Linux
        result = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader"], capture_output=True)
        temperature_str = result.stdout.decode().strip()
        if temperature_str:
            temperature = int(temperature_str)
            return temperature

def get_cpu_load():
    """Get the current CPU load as a percentage."""
    return psutil.cpu_percent()

def get_cpu_frequency():
    """Get the current CPU frequency in MHz."""
    freq = psutil.cpu_freq()
    if freq:
        return freq.current

def get_cpu_cores():
    """Get the number of CPU cores."""
    return psutil.cpu_count(logical=False)

def get_cpu_threads():
    """Get the number of CPU threads."""
    return psutil.cpu_count()

def get_ram_speed():
    """Get the RAM speed in MHz."""
    if platform.system() == "Windows":
        wmi_obj = wmi.WMI(namespace="root\\CIMV2")
        for mem in wmi_obj.query("SELECT * FROM Win32_PhysicalMemory"):
            return int(mem.Speed)
    else:
        with open("/sys/bus/platform/drivers/coretemp/coretemp.0/hwmon/hwmon0/modalias", "r") as f:
            modalias = f.read().strip()
            if "dmi:" in modalias:
                dmi_id = modalias.split("dmi:")[1]
                for filename in os.listdir("/sys/devices/platform"):
                    if dmi_id in filename:
                        with open(f"/sys/devices/platform/{filename}/dmi/id/product_name", "r") as f2:
                            product_name = f2.read().strip().lower()
                            if "thinkpad" in product_name:
                                with open(f"/sys/devices/platform/{filename}/memory_bandwidth", "r") as f3:
                                    return int(f3.read().strip()) / 1000

def get_cpu_info():
    cpu_info = {}
    with open("/proc/cpuinfo", "r") as f:
        for line in f:
            if "model name" in line:
                cpu_info["model_name"] = line.split(":")[1].strip()
            elif "cpu cores" in line:
                cpu_info["cores"] = line.split(":")[1].strip()
            elif "cpu MHz" in line:
                cpu_info["clock_speed"] = line.split(":")[1].strip()
            elif "cache size" in line:
                cpu_info["cache_size"] = line.split(":")[1].strip()
    return cpu_info

def get_gpu_info():
    gpu_info = {}
    try:
        process = subprocess.Popen(["lspci", "-v"], stdout=subprocess.PIPE)
        output, error = process.communicate()
        for line in output.decode().split("\n"):
            if "VGA compatible controller" in line:
                gpu_info["model_name"] = line.split(":")[2].strip()
            elif "Memory" in line:
                gpu_info["memory_size"] = line.split(":")[1].strip()
            elif "clock" in line:
                gpu_info["clock_speed"] = line.split(":")[1].strip()
    except FileNotFoundError:
        pass
    return gpu_info

def get_battery_status():
    battery_status = {}
    battery = psutil.sensors_battery()
    if battery:
        battery_status["percent"] = battery.percent
        battery_status["time_left"] = battery.secsleft
        battery_status["power_plugged"] = battery.power_plugged
    return battery_status

def get_power_status():
    power_status = {}
    c = wmi.WMI()
    for battery in c.Win32_Battery():
        power_status["battery_status"] = battery.Status
        power_status["battery_remaining"] = battery.EstimatedChargeRemaining
        power_status["power_plugged"] = battery.PowerPlugged
    return power_status

def get_timezone():
    timezone = {}
    timezone["timezone"] = platform.timezone()
    timezone["timezone_name"] = time.tzname[0]
    timezone["dst"] = time.daylight
    return timezone

def get_keyboard_layout():
    keyboard_layout = {}
    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Keyboard Layout")
    keyboard_layout["layout_name"] = winreg.QueryValueEx(reg_key, "Layout Text")[0]
    keyboard_layout["layout_id"] = winreg.QueryValueEx(reg_key, "Layout ID")[0]
    return keyboard_layout

def get_screen_resolution():
    screen_resolution = {}
    try:
        output = subprocess.check_output("xrandr | grep \* | cut -d' ' -f4", shell=True)
        output = output.decode().strip()
        screen_resolution["resolution"] = output
    except subprocess.CalledProcessError:
        pass
    return screen_resolution

def get_os_info():
    os_info = {}
    os_info["name"] = os.name
    os_info["system"] = platform.system()
    os_info["release"] = platform.release()
    os_info["version"] = platform.version()
    os_info["architecture"] = platform.architecture()
    os_info["processor"] = platform.processor()
    return os_info

def get_network_info():
    network_info = {}
    hostname = socket.gethostname()
    network_info["hostname"] = hostname
    network_info["IP address"] = socket.gethostbyname(hostname)
    network_info["MAC address"] = ":".join([f"{uuid.getnode():012X}"[i:i+2] for i in range(0, 12, 2)])
    return network_info

def get_memory_info():
    memory_info = {}
    svmem = psutil.virtual_memory()
    memory_info["total"] = svmem.total
    memory_info["available"] = svmem.available
    memory_info["used"] = svmem.used
    memory_info["free"] = svmem.free
    memory_info["percent"] = svmem.percent
    return memory_info

def get_boot_time():
    boot_time = psutil.boot_time()
    return datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")

def get_battery_info():
    battery_info = {}
    battery = psutil.sensors_battery()
    if battery:
        battery_info["percent"] = battery.percent
        battery_info["time left"] = seconds_to_time_string(battery.secsleft)
        battery_info["power plugged"] = battery.power_plugged
    return battery_info

def get_disk_usage(path="."):
    disk_usage = {}
    disk = psutil.disk_usage(path)
    disk_usage["total"] = disk.total
    disk_usage["used"] = disk.used
    disk_usage["free"] = disk.free
    disk_usage["percent"] = disk.percent
    return disk_usage

def get_process_info():
    process_info = []
    for process in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        process_info.append({
            "pid": process.info["pid"],
            "name": process.info["name"],
            "cpu_percent": process.info["cpu_percent"],
            "memory_percent": process.info["memory_percent"]
        })
    return process_info

def get_cpu_temperature():
    cpu_temp = None
    if platform.system() == "Windows":
        try:
            w = wmi.WMI(namespace="root\OpenHardwareMonitor")
            temperature_sensors = w.Sensor()
            cpu_temp = next((sensor.Value for sensor in temperature_sensors if sensor.Name == "CPU Package"), None)
            cpu_temp = round(cpu_temp, 2) if cpu_temp is not None else None
        except Exception:
            pass
    elif platform.system() == "Linux":
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as f:
                cpu_temp = float(f.read().strip()) / 1000.0
        except Exception:
            pass
    return cpu_temp

def get_time_zone():
    time_zone = None
    if platform.system() == "Windows":
        time_zone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
    elif platform.system() == "Linux":
        try:
            output = subprocess.check_output(["timedatectl", "status"], stderr=subprocess.DEVNULL)
            time_zone = next((line.split(":")[1].strip() for line in output.decode().splitlines() if line.startswith("Time zone")), None)
        except Exception:
            pass
    return time_zone

def get_battery_capacity():
    battery_capacity = None
    if platform.system() == "Windows":
        battery_capacity = ctypes.c_long()
        ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(battery_capacity))
        battery_capacity = battery_capacity.value
    elif platform.system() == "Linux":
        try:
            with open("/sys/class/power_supply/BAT0/charge_full") as f:
                battery_capacity = int(f.read().strip()) / 1000.0
        except Exception:
            pass
    return battery_capacity

def get_cpu_usage():
    cpu_usage = {}
    if platform.system() == "Windows":
        try:
            w = wmi.WMI()
            cpu_usage["usage"] = round(w.Win32_Processor()[0].LoadPercentage, 2)
        except Exception:
            pass
    elif platform.system() == "Linux":
        try:
            cpu_usage["usage"] = round(psutil.cpu_percent(), 2)
        except Exception:
            pass
    return cpu_usage

def get_language():
    language = None
    try:
        language, _ = locale.getdefaultlocale()
    except Exception:
        pass
    return language
