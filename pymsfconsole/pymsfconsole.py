#! /usr/bin/env python3
import pexpect
from queue import Queue
from queue import Empty as QueueEmpty
from time import sleep
import socket

def enqueue_stdout(spawn, stdout_q):
    while (True):
        temp = spawn.readline().decode()
        if (temp != ""):
            stdout_q.put(temp)

spawn = pexpect.spawn("msfconsole")
stdout_q = Queue()
try:
    _thread.start_new_thread(enqueue_stdout, (spawn, stdout_q))
except:
    print("\nERROR: Unable to start thread. Try running with `sudo`")
    exit(1)
print("success")
exit()

















import pexpect
import _thread
from queue import Queue
from queue import Empty as QueueEmpty
from time import sleep
import sys

def enqueue_stdout(spawn, stdout_q):
    while (True):
        temp = spawn.readline().decode()
        if (temp != ""):
            stdout_q.put(temp)

spawn = pexpect.spawn("msfconsole")
stdout_q = Queue()
try:
    _thread.start_new_thread(enqueue_stdout, (spawn, stdout_q))
except:
    print("\nERROR: Unable to start thread. Try running with `sudo`")
    exit(1)
sleep(10)
while (True):
    try:
        print(stdout_q.get_nowait(), end="")
    except (QueueEmpty):
        break
    sleep(0.1)
temp = spawn.read(26).decode()
print(temp)
#for c in temp:
    #print(ord(c))
    #if (ord(c) > 31):
    #print(c, end="")
    #print(c)
#print(spawn.read(1).decode(), end="")
print()
sys.stdout.flush()
print("ending")
exit()
























import pexpect
from queue import Queue
from queue import Empty as QueueEmpty
from time import sleep
import socket

def enqueue_stdout(spawn, stdout_q):
    while (True):
        temp = spawn.readline().decode()
        if (temp != ""):
            stdout_q.put(temp)

spawn = pexpect.spawn("msfconsole")
stdout_q = Queue()
try:
    _thread.start_new_thread(enqueue_stdout, (spawn, stdout_q))
except:
    print("\nERROR: Unable to start thread. Try running with `sudo`")
    exit(1)
print("success")

    
states_and_transitions = [
    ["recon", ["recon", "inital_intrusion"]],
    ["initial_intrusion", ["discovery", "privilege_escalation"]],
    ["discovery", ["discovery", "privilege_escalation", "data_exfiltration"]],
    ["privilege_escalation", ["discovery", "persistence"]],
    ["persistence", ["discovery", "privilege_escalation", "persistence"]],
    ["data_exfiltration", ["discovery", "privilege_escalation", "persistence"]]
    ]

victim_ip = ""
while (True):
    victim_ip = input("Please enter victim IP address: ")
    try:
        socket.inet_aton(victim_ip)
        break
    except:
        print("\tERROR: Invalid IP address.")

print(victim_ip)

#sleep(10)
while (True):
    try:
        print(stdout_q.get_nowait(), end="")
    except (QueueEmpty):
        break
    #sleep(0.1)
temp = spawn.read(26).decode()
print(temp)
















































    






            
def terminal(stdout_q):
    status = 0
    input_str = ""
    while (True):
        temp = ""
        while (True):
            try:
                temp += stdout_q.get(block=False, timeout=1)
            except (QueueEmpty):
                break
        if (temp == ""):
            temp = "$ "
        input_str = input(temp)
        if (input_str == "exit"):
            status = 1
            break
        elif (input_str == "pause"):
            status = 2
            break
        else:
            spawn.sendline((input_str + "\n").encode())
            
    return status
        

spawn = pexpect.spawn("msfconsole")
sleep(10)
print(spawn.expect([pexpect.EOF, "msf >".encode()]))
exit()




#spawn.interact()
#spawn.close()
#sleep(1)
#print("\nsuccess")
#exit()




stdout_q = Queue()
try:
    _thread.start_new_thread(enqueue_stdout, (spawn, stdout_q))
except:
    print("\nERROR: Unable to start thread. Try running with `sudo`")
    exit(1)
sleep(1)
while (True):
    temp = ""
    try:
        temp = stdout_q.get_nowait()
    except (QueueEmpty):
        pass
    if (temp != ""):
        print(temp, end="")
exit()
















while (True):
    temp = ""
    while (True):
        try:
            temp_char = stdout_q.get_nowait()
            temp += temp_char
        except (QueueEmpty):
            break
    if (temp != ""):
        print(temp)
    else:
        break
    sleep(2)

print(spawn.read(5).decode())
print("\nending")
exit()





#for _ in range(10):
    #sleep(1)
while (True):
    try:
        print(stdout_q.get_nowait(), end="")
    except (QueueEmpty):
        break
print("\nsuccess")
exit()
    
while (True):
    status = terminal(stdout_q)
    if (status == 1):
        break
    elif (status == 2):
        while (True):
            temp_input = input("Next command: ")
            if (temp_input == "resume"):
                break
            else:
                print("\t" + temp_input)

