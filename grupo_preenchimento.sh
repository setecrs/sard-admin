#!/bin/bash -e
if [ "$1" == "" ]
then
	echo Utilize $0 GRUPO 
	echo 
	exit 1
fi

GRUPO="$1"


smbldap-groupshow "$GRUPO" | grep memberUid | awk '{ split($2,a,","); i=1; while ( i<= length(a) ) { print "*********  preenchendo perfil do usuario "a[i]" *********"; system("/root/scripts/sard/usuario_preenchimento.sh "a[i]); i++; }}' &&  echo "******** Finalizado Ajustes do Grupo *********" || ( echo "Falha" && exit 1 )


