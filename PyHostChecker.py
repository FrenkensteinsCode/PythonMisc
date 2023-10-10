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

# Input
target = input("Hostname/IP: ")
port_range = input("Port-Range: ")

start_p, end_p = port_range.split("-")
start_p, end_p = int(start_p), int(end_p)

ports = [ p for p in range(start_p, end_p)]

# Info
print(f"-" * 50)
print(f"Scanning Target: " + target)
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

