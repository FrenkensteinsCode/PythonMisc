# PythonMisc
Miscellaneous Python scripts serving different purposes

## PyHostChecker.py ##
- Host- and Port-Scanner
- Checks if target is online and which ports are accessible
- Maps port number to service-name
  
#### Usage
- Install prerequisites
  - <code>pip install colorama pyfiglet</code>
- Download or clone the script to your local disk
  - Execute the script: <code>python ./PyHostChecker.py</code>
- You will be prompted to enter a target-host (hostname/ip) and a port-range

#### Considerations
This script has been tested on the following platforms:
- Windows 10 (22H2) - Python 3.11.2
  - WSL (kali-rolling 2024.2) - Python 3.11.8

## PyBench.py
- Benchmark for CPU and IO
- Utilizes the Sieve of Eratosthenes for benchmarking the CPU

#### Usage
- Install prerequisites
  - <code>pip3 install tdqm</code>
- Adjust the values &lt;limit&gt; and &lt;repeats&gt; to your needs
- Download or clone the script to your local disk
  - Execute the script: <code>python3 ./PyBench.py</code>

#### Considerations
This script has been tested on the following platforms:
- Windows 10 (22H2) - Python 3.11.2
  - WSL (kali-rolling 2024.4) - Python 3.12.8