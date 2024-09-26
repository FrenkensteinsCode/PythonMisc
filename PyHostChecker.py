
from colorama import init, Fore
from datetime import datetime
import platform
import pyfiglet
from queue import Queue
import socket
import subprocess
from threading import Thread, Lock

# Banner
ascii_banner = pyfiglet.figlet_format("PyHostChecker")
print(ascii_banner)

# Colourization of output
init()
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET

q = Queue()
print_lock = Lock()

# DNS lookup helper functions
def get_domain_name(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return hostname
    except socket.herror:
        return "No DNS entry found!"
    
def get_ip_address(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.herror:
        return "No DNS entry found!"

# Input
target = input("Hostname/IP: ")
port_range = input("Port-Range: ")

if ("-" not in port_range):
    start_p = end_p = int(port_range)
else:
    start_p, end_p = map(int, port_range.split("-"))

ports = [p for p in range(start_p, end_p + 1)]

# Info
print(f"-" * 50)
print(f"Scanning Target: " + target + " (" + get_domain_name(target) + " / " + get_ip_address(target) + ")")
print(f"Scanning started at: " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
print(f"-" * 50)

# Ping logic
def ping():
    ''' Pings a target-host for one iteration to see if it's online '''

    param = "-n" if platform.system() == "Windows" else "-c"
    cmd = ["ping", param, "1", target]

    HOST_UP = True if subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0 else False

    if (HOST_UP == True):
        print(f"{target} seems to be up and running \u2705")
    else:
        print(f"{target} seems to be down \u274C")

# Port scan logic
def port_scan(port):
    ''' Scans open ports on target-host to see if they're open 
    
        Input:
            port: Port to be checked against
    '''

    try:
        s = socket.socket()
        s.connect((target,port))
    except:
        with print_lock:
            print(f"{RED}{target:15}:{port:5} is closed {RESET}", end='\r')
    else:
        with print_lock:
            print(f"{GREEN}{target:15}:{port:5} is open{RESET}{GREEN} => {socket.getservbyport(port, 'tcp')}")
    finally:
        s.close()

# Parallelization
def scan_thread():
    global q
    while True:
        worker = q.get()
        port_scan(worker)
        q.task_done()


def scan(ports):
    global q
    THREADS = 200
    for t in range(THREADS):
        t = Thread(target=scan_thread)
        t.daemon = True
        t.start()
    for worker in ports:
        q.put(worker)
    q.join()


def main():
    ping()
    scan(ports)

if __name__ == "__main__":
    main()
