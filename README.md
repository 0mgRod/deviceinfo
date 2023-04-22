# dvinfo

### Installation

```
pip install dvinfo
```

### Documentation:

```py
import dvinfo

# Get the current CPU temperature
cpu_temperature = dvinfo.get_cpu_temperature()

# Get the current GPU temperature
gpu_temperature = dvinfo.get_gpu_temperature()

# Get the current CPU load as a percentage
cpu_load = dvinfo.get_cpu_load()

# Get the current CPU frequency in MHz
cpu_frequency = dvinfo.get_cpu_frequency()

# Get the number of CPU cores
cpu_cores = dvinfo.get_cpu_cores()

# Get the number of CPU threads
cpu_threads = dvinfo.get_cpu_threads()

# Get the RAM speed in MHz
ram_speed = dvinfo.get_ram_speed()

# Get CPU information such as model name, cores, clock speed, and cache size
cpu_info = dvinfo.get_cpu_info()

# Get GPU information such as model name, memory size, and clock speed
gpu_info = dvinfo.get_gpu_info()

# Get the battery status such as the percentage, time left, and power plugged status
battery_status = dvinfo.get_battery_status()

# Get the power status such as the battery status, battery remaining, and power plugged status
power_status = dvinfo.get_power_status()

# Get the timezone and timezone name
timezone = dvinfo.get_timezone()
```

#### get_cpu_temperature() -> float
Get the current CPU temperature in degrees Celsius.

#### get_gpu_temperature() -> float
Get the current GPU temperature in degrees Celsius.

#### get_cpu_load() -> float
Get the current CPU load as a percentage.

#### get_cpu_frequency() -> float
Get the current CPU frequency in MHz.

#### get_cpu_cores() -> int
Get the number of CPU cores.

#### get_cpu_threads() -> int
Get the number of CPU threads.

#### get_ram_speed() -> int
Get the RAM speed in MHz.

#### get_cpu_info() -> dict
Get CPU information such as model name, cores, clock speed, and cache size.

#### get_gpu_info() -> dict
Get GPU information such as model name, memory size, and clock speed.

#### get_battery_status() -> dict
Get the battery status such as the percentage, time left, and power plugged status.

#### get_power_status() -> dict
Get the power status such as the battery status, battery remaining, and power plugged status.

#### get_timezone() -> dict
Get the timezone and timezone name.
