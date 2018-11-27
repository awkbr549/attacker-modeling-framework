#! /bin/bash

IP=$TARGET

echo "nmap -sV -Pn -T5 $IP"

nmap -sV -Pn -T4 $IP
