#!/bin/bash -e

: ${LDAP_ADMIN_PASSWORD?-LDAP_ADMIN_PASSWORD not set}
: ${LDAP_BASE_DN?-LDAP_BASE_DN not set}
: ${LDAP_SERVER?-LDAP_SERVER not set}

sed -i -e 's|passdb backend.*|passdb backend = ldapsam:"ldap://'${LDAP_SERVER}'"|' /etc/samba/smb.conf

sed -i -e 's|masterLDAP=.*|masterLDAP="'${LDAP_SERVER}'"|' /etc/smbldap-tools/smbldap.conf
sed -i -e 's|slaveLDAP=.*|slaveLDAP="'${LDAP_SERVER}'"|' /etc/smbldap-tools/smbldap.conf

cat > /etc/smbldap-tools/smbldap_bind.conf <<EOF
slaveDN="cn=admin,${LDAP_BASE_DN}"
slavePw="${LDAP_ADMIN_PASSWORD}"
masterDN="cn=admin,${LDAP_BASE_DN}"
masterPw="${LDAP_ADMIN_PASSWORD}"
EOF

cat > /etc/sssd/sssd.conf <<EOF
[domain/default]

autofs_provider = ldap
enumerate = True
cache_credentials = True
krb5_realm = #
ldap_search_base = dc=setecrs,dc=dpf,dc=gov,dc=br
id_provider = ldap
auth_provider = ldap
chpass_provider = ldap
ldap_uri = ldap://${LDAP_SERVER}/
ldap_tls_cacertdir = /etc/openldap/cacerts
ldap_id_use_start_tls = False
entry_cache_timeout = 5
ldap_default_bind_dn = cn=admin,${LDAP_BASE_DN}
ldap_default_authtok_type = password
ldap_default_authtok = ${LDAP_ADMIN_PASSWORD}

[sssd]
services = nss, pam, autofs
config_file_version = 2
domains = default

[nss]

[pam]

[sudo]

[autofs]

[ssh]

[pac]
EOF

chmod 600 /etc/sssd/sssd.conf

if [ -e /var/run/sssd.pid ]
then
  SSSDPID=`cat /var/run/sssd.pid`
  # test if the process died
  if kill -0 $SSSDPID 2>/dev/null
  then
    echo -n
  else
    rm /var/run/sssd.pid
    sssd -D
  fi
else # /var/run/sssd.pid does not exist
  sssd -D
fi

if [ ! -e /var/lib/samba/private/secrets.tdb ]
then
  : ${SID?-SID not set}
  net setlocalsid $SID
  smbpasswd -w $LDAP_ADMIN_PASSWORD
fi

# wait for ldap
while ! smbldap-userlist
do
  sleep 0.1
done

# different passwords on purpose, so we don't change the root password
(echo 1; echo 2) | smbldap-populate

exec "$@"
