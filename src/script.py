import os
import sys
import socket
import threading
from queue import Queue
import time
import re
import subprocess

all_library = ["colorama", "psutil"]

for library in all_library:
    try:
        __import__(library)
    except ImportError:
        print(f"Library {library} not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", library])
        os.system('cls' if os.name == 'nt' else 'clear')

from colorama import Fore, Style, init
import psutil

init(autoreset=True)

THREADS = 50
MAX_THREADS = 100
lock = threading.Lock()
scan_results = {}

def print_logo():
    texts = (f"\n"
            f"   {Fore.YELLOW}{Style.BRIGHT}Port Scanner Tool:\n"
            f"     {Fore.GREEN}[+] Created by B-3dev\n"
            f"     {Fore.WHITE}[+] Telegram: @B3dev\n"
            f"     {Fore.RED}[+] GitHub: b-3dev/Port-Scanner\n"
            )
    print(texts)

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            with lock:
                if result == 0:
                    scan_results[port] = 'OPEN'
                else:
                    scan_results[port] = 'CLOSED'
    except socket.error:
        pass

def threader(queue, ip, total_ports, semaphore):
    while True:
        semaphore.acquire()
        port = queue.get()
        scan_port(ip, port)
        queue.task_done()
        semaphore.release()
        print_progress(queue.qsize(), total_ports)

def print_progress(remaining_ports, total_ports):
    progress = (total_ports - remaining_ports) / total_ports
    bar_length = 50
    block = int(round(bar_length * progress))
    progress_bar = f"=> [{'#' * block}{' ' * (bar_length - block)}] >"
    print(f"\r{progress_bar}", end="")

def scan(ip, start_port, end_port):
    queue = Queue()
    total_ports = end_port - start_port + 1
    semaphore = threading.Semaphore(MAX_THREADS)
    for _ in range(THREADS):
        thread = threading.Thread(target=threader, args=(queue, ip, total_ports, semaphore))
        thread.daemon = True
        thread.start()
    for port in range(start_port, end_port + 1):
        queue.put(port)
    queue.join()

def is_valid_ip_or_domain(ip):
    if not ip or ip.strip() == "":
        return False

    if '..' in ip or ip.startswith('.') or ip.endswith('.'):
        return False

    if re.search(r'[\u0600-\u06FF\u2000-\u206F\u2D80-\u2DDF\uFB00-\uFB4F]', ip):
        print(Fore.RED + "Invalid character in domain. BIDI violation or unsupported characters.")
        return False

    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        pass

    try:
        socket.gethostbyname(ip)
        return True
    except socket.error:
        return False

def validate_port_input(prompt):
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input.isdigit():
                port = int(user_input)
                if 1 <= port <= 65535:
                    return port
                else:
                    print(Fore.RED + "Port number must be between 1 and 65535.")
            else:
                print(Fore.RED + "Invalid input. Please enter a valid integer.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid integer.")

def validate_ip_or_domain_input():
    while True:
        target = input(Fore.CYAN + "Enter IP address or domain to scan: ").strip()
        if target and is_valid_ip_or_domain(target):
            return target
        else:
            print(Fore.RED + "Invalid IP/domain. Please enter a valid one.")

def print_system_info(start_time, num_open_ports, num_ports_scanned):
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()

    uptime = time.time() - start_time
    process_info = {
        'Memory Usage': f"{memory_info.rss / 1024 / 1024:.2f} MB",
        'Process ID': process.pid,
        'Process Name': process.name(),
        'Threads': threading.active_count(),
        'Open Ports': num_open_ports,
        'Closed Ports': num_ports_scanned - num_open_ports,
        'Total Ports Scanned': num_ports_scanned,
        'Scan Duration': f"{uptime:.2f} seconds"
    }

    print(f"\n{Fore.GREEN}{Style.BRIGHT}Process Information:")
    for key, value in process_info.items():
        print(f" - {Fore.YELLOW}{key}: {Fore.WHITE}{value}")

def main():
    print_logo()

    while True:
        target = validate_ip_or_domain_input()

        start_port = validate_port_input(Fore.CYAN + "Enter start port number: ")
        end_port = validate_port_input(Fore.CYAN + "Enter end port number: ")

        if start_port >= end_port:
            print(Fore.RED + "Start port must be less than end port. Please enter again.")
            continue

        print(Fore.GREEN + f"\nStarting scan for {target} from port {start_port} to {end_port}...")

        start_time = time.time()
        num_open_ports = 0
        num_ports_scanned = 0

        try:
            scan(target, start_port, end_port)

            print("\r" + " " * 60, end="")

            for port in range(start_port, end_port + 1):
                if port in scan_results:
                    num_ports_scanned += 1
                    if scan_results[port] == 'OPEN':
                        num_open_ports += 1

            if num_open_ports == 0:
                print(f"\n{Fore.RED}No open ports found.")
            else:
                print(f"\n{Fore.GREEN}Scan completed successfully.")

            if num_ports_scanned == 0:
                print(f"\n{Fore.RED}No ports were scanned. Check the range or try a different target.")

            if num_open_ports > 0:
                print(f"\n{Fore.GREEN}{Style.BRIGHT}Open ports:")
                for port in range(start_port, end_port + 1):
                    if port in scan_results and scan_results[port] == 'OPEN':
                        print(f" - {Fore.GREEN}{port}")

            print_system_info(start_time, num_open_ports, num_ports_scanned)

        except Exception as e:
            print(Fore.RED + f"Error during scan: {e}")

if __name__ == "__main__":
    main()
