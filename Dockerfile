FROM fedora:28

RUN dnf makecache
RUN dnf install -y samba smbldap-tools sssd-ldap findutils python3

COPY docker/smb.conf /etc/samba/
COPY docker/smbldap.conf /etc/smbldap-tools/

WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install waitress wheel -r requirements.txt
COPY . .
RUN python3 setup.py bdist_wheel
RUN python3 -m pip install /app/dist/*.whl

COPY docker/entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

CMD ["waitress-serve", "--port=80", "--call", "sardadmin:app.create_app"]
