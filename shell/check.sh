#!/bin/bash
echo 'check online begin'
root=`sed '/^#/d' /etc/myap.conf | grep '^root' | awk -F '=' '{print $2}'`
online=`find $root -name online.db`
cd $root
iplist=`cat $online | awk '{print $3}' | sed -e '1d'`
if [ -f "ping" ]; then
	rm ping
fi
cp $online tmp
for ip in $iplist; do
	a=`ping -c 4 $ip | grep loss | awk '{print $4}'`
	if [[ $a < 2 ]]; then
		sed "/$ip/d" tmp > tmpa
		mv tmpa tmp
	fi
	echo -e "$ip\t$a" >>ping
done

cp tmp $online
rm tmp
rm ping
echo 'check online end'
