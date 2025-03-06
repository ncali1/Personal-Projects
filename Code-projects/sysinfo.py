import platform
import psutil
import subprocess
import time
import matplotlib.pyplot as plt
from collections import deque

def get_computer_system_info():
    system_info = {}

    # Get platform info
    system_info['platform'] = platform.system()
    system_info['platform_version'] = platform.version()
    system_info['platform_release'] = platform.release()
    system_info['architecture'] = platform.machine()
    system_info['hostname'] = platform.node()
    system_info['processor'] = platform.processor()

    # Get CPU info
    cpu = {}
    cpu['physical_cores'] = psutil.cpu_count(logical=False)
    cpu['total_cores'] = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    cpu['max_freq'] = cpu_freq.max
    cpu['min_freq'] = cpu_freq.min
    cpu['current_freq'] = cpu_freq.current
    cpu['usage'] = psutil.cpu_percent(interval=1)
    system_info['cpu'] = cpu

    # Get RAM Info
    vram = psutil.virtual_memory()
    ram_info = {}
    ram_info['total'] = vram.total
    ram_info['available'] = vram.available
    ram_info['used'] = vram.used
    ram_info['percentage'] = vram.percent

    # Get RAM speed on macOS
    if system_info['platform'] == 'Darwin':  # macOS
        try:
            output = subprocess.check_output(['system_profiler', 'SPMemoryDataType'])
            output = output.decode('utf-8')
            for line in output.split('\n'):
                if 'Speed' in line:
                    ram_info['speed'] = line.split(':')[-1].strip()
                    break
        except subprocess.CalledProcessError as e:
            ram_info['speed'] = 'Unknown'

    system_info['ram_info'] = ram_info

    return system_info

def print_system_info(system_info):
    print('\n')
    print("System Information")
    print("==================")
    print(f"Platform: {system_info['platform']}")
    print(f"Platform Version: {system_info['platform_version']}")
    print(f"Platform Release: {system_info['platform_release']}")
    print(f"Architecture: {system_info['architecture']}")
    print(f"Hostname: {system_info['hostname']}")
    print(f"Processor: {system_info['processor']}")
    print("\nCPU Information")
    print("==================")
    print(f"Physical Cores: {system_info['cpu']['physical_cores']}")
    print(f"Total Cores: {system_info['cpu']['total_cores']}")
    print(f"Max Frequency: {system_info['cpu']['max_freq']} MHz")
    print(f"Min Frequency: {system_info['cpu']['min_freq']} MHz")
    print(f"Current Frequency: {system_info['cpu']['current_freq']} MHz")
    print(f"CPU Usage: {system_info['cpu']['usage']}%")
    print("\nRAM Information")
    print("==================")
    print(f"Total: {system_info['ram_info']['total'] / (1024 ** 3):.2f} GB")
    print(f"Available: {system_info['ram_info']['available'] / (1024 ** 3):.2f} GB")
    print(f"Used: {system_info['ram_info']['used'] / (1024 ** 3):.2f} GB")
    print(f"Percentage: {system_info['ram_info']['percentage']}%")
    if 'speed' in system_info['ram_info']:
        print(f"Speed: {system_info['ram_info']['speed']}")

def plot_real_time_data():
    plt.ion()  # Turn on interactive mode
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    cpu_freqs = deque(maxlen=60)
    ram_usages = deque(maxlen=60)
    times = deque(maxlen=60)

    start_time = time.time()

    try:
        while True:
            system_info = get_computer_system_info()
            current_time = time.time() - start_time

            cpu_freqs.append(system_info['cpu']['current_freq'])
            ram_usages.append(system_info['ram_info']['percentage'])
            times.append(current_time)

            ax1.clear()
            ax2.clear()

            ax1.plot(times, cpu_freqs, label='CPU Frequency (MHz)')
            ax2.plot(times, ram_usages, label='RAM Usage (%)')

            ax1.set_title('Real-Time CPU Frequency')
            ax1.set_xlabel('Time (s)')
            ax1.set_ylabel('Frequency (MHz)')
            ax1.legend()

            ax2.set_title('Real-Time RAM Usage')
            ax2.set_xlabel('Time (s)')
            ax2.set_ylabel('Usage (%)')
            ax2.legend()

            plt.tight_layout()
            plt.pause(1)  # Update every second
    except KeyboardInterrupt:
        print("Program terminated.")
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    system_info = get_computer_system_info()
    print_system_info(system_info)

    user_input = input("Do you want to see the real-time line graph? (y/n): ").strip().lower()
    if user_input == 'y':
        plot_real_time_data()
    elif user_input == 'n':
        print("Exiting the program.")
    else:
        print("Invalid input. Exiting the program.")