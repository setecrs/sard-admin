#!/bin/bash -ex
USER="${1?Utilize $0 USUARIO}"
SENHA=$(cat /dev/urandom | tr -dc a-z0-9 | head -c6)

smbldap-groupadd -a "$USER"
smbldap-useradd -a -g "$USER" -s /bin/false -m "$USER"
smbldap-usermod --shadowMax 3650 "$USER"
echo $SENHA | smbldap-passwd -p "$USER"
mkdir -p /home/"$USER"/Desktop/operacoes
chown -R "$USER":"$USER" /home/"$USER"
smbldap-groupmod -m "$USER" Domain_Users
echo senha: $SENHA
