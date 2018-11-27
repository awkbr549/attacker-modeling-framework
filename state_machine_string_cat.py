#! /usr/bin/python3

###
# State Machine
###

# initial_instruction --> persistence
# persistence --> ping_home

from os import getcwd
import subprocess

def get_option():
    print("\tPlease enter an option: ")
    print("\t\t1 - option1")
    print("\t\t2 - option2")
    print("\t\t3 - option3")
    return input()

def get_next_state(state=""):
    return_str = ""
    print("\tPlease enter the next state: ")
    if (state == "initial_intrusion"):
        print("\t\t1 - persistence")
        print("\t\t2 - local_priv_esc")
        print("\t\t3 - exit")
        temp_input = int(input())
        if (temp_input == 1):
            return_str = "persistence"
        elif (temp_input == 2):
            return_str = "local_priv_esc"
        elif (temp_input == 3):
            return_str = "exit"

    elif (state == "persistence"):
        print("\t\t1 - ping_home")
        print("\t\t2 - local_recon")
        print("\t\t3 - exit")
        temp_input = int(input())
        if (temp_input == 1):
            return_str = "ping_home"
        elif (temp_input == 2):
            return_str = "local_recon"
        elif (temp_input == 3):
            return_str = "exit"

    elif (state == "ping_home"):
        print("\t\t1 - persistence")
        print("\t\t2 - exit")
        temp_input = int(input())
        if (temp_input == 1):
            return_str = "persistence"
        elif (temp_input == 2):
            return_str = "exit"

    elif (state == "dump_creds"):
        print("\t\t1 - net_recon")
        print("\t\t2 - exit")
        temp_input = int(input())
        if (temp_input == 1):
            return_str = "net_recon"
        elif (temp_input == 2):
            return_str = "exit"

    elif (state == "local_priv_esc"):
        print("\t\t1 - persistence")
        print("\t\t2 - dump_creds")
        print("\t\t3 - local_recon")
        print("\t\t4 - net_recon")
        print("\t\t5 - exit")
        temp_input = int(input())
        if (temp_input == 1):
            return_str = "persistence"
        elif (temp_input == 2):
            return_str = "dump_creds"
        elif (temp_input == 3):
            return_str = "local_recon"
        elif (temp_input == 4):
            return_str = "net_recon"
        elif (temp_input == 5):
            return_str = "exit"

    elif (state == "local_recon"):
        print("\t\t1 - local_priv_esc")
        print("\t\t2 - net_recon")
        print("\t\t3 - package")
        print("\t\t4 - exit")
        temp_input = int(input())
        if (temp_input == 1):
            return_str = "local_priv_esc"
        elif (temp_input == 2):
            return_str = "net_recon"
        elif (temp_input == 3):
            return_str = "package"
        elif (temp_input == 4):
            return_str = "exit"

    elif (state == "net_recon"):
        print("\t\t1 - remote_exec")
        print("\t\t2 - exit")
        temp_input = int(input())
        if (temp_input == 1):
            return_str = "remote_exec"
        elif (temp_input == 2):
            return_str = "exit"

    elif (state == "remote_exec"):
        print("\t\t1 - persistence")
        print("\t\t2 - local_recon")
        print("\t\t3 - package")
        print("\t\t4 - exit")
        temp_input = int(input())
        if (temp_input == 1):
            return_str = "persistence"
        elif (temp_input == 2):
            return_str = "local_recon"
        elif (temp_input == 3):
            return_str = "package"
        elif (temp_input == 4):
            return_str = "exit"

    elif (state == "exfil"):
        print("\t\t1 - exit")
        temp_input = int(input())
        if (temp_input == 1):
            return_str = "exit"

    elif (state == "package"):
        print("\t\t1 - exfil")
        print("\t\t2 - exit")
        temp_input = int(input())
        if (temp_input == 1):
            return_str = "exfil"
        elif (temp_input == 2):
            return_str = "exit"

    return return_str

def run_state(state=""):
    print("STATE: " + state)
    subprocess.call([getcwd() + "/" + state + "/option" + get_option() + ".sh"])
    return get_next_state(state)

next_state = run_state("initial_intrusion")
while (True):
    if (next_state == "exit"):
        break
    next_state = run_state(next_state)