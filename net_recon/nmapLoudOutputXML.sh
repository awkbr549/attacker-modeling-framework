#! /bin/bash

attackerIP=$1

echo "nmap -sV -Pn -T4 -p 1-65535 -oX metasploitable3.xml $attackerIP"
echo "     -sV is version detection (equivalent to -A and -sR"
echo "         -Pn skips initial ping sweep"
echo "             -T4 Aggressive timing"
echo "                 -p scans this port range"
echo "                            -oX results to xml file"


nmap -sV -Pn -T4 -p 1-65535 -oX metasploitable3.xml $attackerIP
