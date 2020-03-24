FROM fedora:28

RUN dnf makecache
RUN dnf install -y samba smbldap-tools sssd-ldap findutils python3

COPY smb.conf /etc/samba/
COPY smbldap.conf /etc/smbldap-tools/

WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY . .

COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

CMD /app/sardrest.py
