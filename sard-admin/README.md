# sard-admin

![sard-admin ci-cd](https://github.com/setecrs/sard-admin/workflows/sard-admin_ci-cd/badge.svg)

REST API that uses smbldap-tools to manage SAMBA/CIFS users and groups in a LDAP database.

It also does permisisons management and make adjustements to the user's home folder.

## Running using docker

    docker run \
      -p 80:80 \
      -e LDAP_SERVER=myldap \
      -e LDAP_BASE_DN=2 \
      -e LDAP_ADMIN_PASSWORD=1 \
      -e SID=S-1-5-21-1-2-3 \
      setecrs/sard-admin

## Running from source

    python3 -m pip install .
    export FLASK_APP=sardadmin
    flask run
