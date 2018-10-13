#! /usr/bin/python

#https://stackoverflow.com/questions/16602513/preventing-linewrap-when-using-pexpect-bash

import pexpect

spawn = pexpect.spawn("/bin/bash")
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

exit()