#!/bin/bash -ex
OP="${1?Utilize $0 OPERACAO}"

smbldap-groupadd "$OP"
mkdir -p /operacoes/"$OP"
chmod -R u=rwX,g=rX,o-rwx /operacoes/"$OP"
chown -R root:"$OP" /operacoes/"$OP"
