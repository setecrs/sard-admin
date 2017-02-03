#!/bin/bash -e
if [ "$1" == "" ]
then
	echo Utilize $0 USUARIO
	echo 
	exit 1
fi

USER="$1"


echo "Ajustando diretorio home:" 
mkdir -p /home/"$USER"/Desktop/operacoes && groups "$USER" | awk '{ split($0,a," "); i=4;  if (length(a)-2>=14){ print "ATENCAO ao numero maximo de grupos (16)!!"; }; while ( i<= length(a) ) { system("ln -sfv /sard/extracao/"a[i]" /home/"a[1]"/Desktop/operacoes/"a[i]); i++; }}' &&  echo "OK" || ( echo "Falha" && exit 1 )

echo -n "Ajustando proprietario e grupo..."
chown -R "$USER":"$USER" /home/"$USER" && echo "OK" || ( echo "Falha" && exit 1 )

