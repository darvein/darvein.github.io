# Linux Battery Administration

## LTP 
LTP is one of the most commons to analyze and manage battery usage in a laptop computer.

yay -S ltp
systemctl enable ltp


Here an config example for /etc/ltp.d/01-custom.conf
```
# TLP Configuration - Optimized for use with auto-cpufreq

# Avoid changing CPU settings to prevent conflicts with auto-cpufreq
# CPU_SCALING_GOVERNOR_ON_AC=performance
# CPU_SCALING_GOVERNOR_ON_BAT=powersave
# CPU_HWP_ON_AC=balance_performance
# CPU_HWP_ON_BAT=balance_power

# Disk Devices: Set disk APM level on battery to 128 and enable spin down after 10 seconds
DISK_APM_LEVEL_ON_BAT="128"
DISK_IDLE_SECS_ON_BAT=10

# SATA aggressive link power management (ALPM):
# min_power for battery, medium_power for AC
SATA_LINKPWR_ON_AC=medium_power
SATA_LINKPWR_ON_BAT=min_power

# Runtime Power Management for PCI(e) devices
RUNTIME_PM_ON_AC=on
RUNTIME_PM_ON_BAT=auto

# USB autosuspend feature
USB_AUTOSUSPEND=1

# Disable Wake On LAN
WOL_DISABLE=Y

# Wi-Fi Power Saving mode: 1=disable, 5=enable
WIFI_PWR_ON_AC=off
WIFI_PWR_ON_BAT=on

# Bluetooth power saving
BLUETOOTH_DISABLE_ON_BAT=1

# Disable autosuspend for specified devices, e.g., wireless mouse or keyboard
#USB_BLACKLIST="1234:5678"

# Enable Audio power saving for Intel HDA, AC97 devices after 1 sec
SOUND_POWER_SAVE_ON_AC=0
SOUND_POWER_SAVE_ON_BAT=1
SOUND_POWER_SAVE_CONTROLLER=Y

# Power off optical drive in UltraBay/MediaBay when running on battery
BAY_POWEROFF_ON_BAT=1
BAY_DEVICE="sr0"

```

## Auto-cpufreq
Auto-cpufreq is a tool to manage the CPU frequency and power usage.
yay -S auto-cpufreq
systemctl enable auto-cpufreq

