FROM python:3.6-alpine as build
WORKDIR /app
RUN python3 -m pip install wheel
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY . .
RUN python3 setup.py bdist_wheel

FROM fedora:28

RUN dnf makecache
RUN dnf install -y samba smbldap-tools sssd-ldap findutils python3

COPY docker/smb.conf /etc/samba/
COPY docker/smbldap.conf /etc/smbldap-tools/
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY --from=build /app /app
RUN python3 -m pip install /app/dist/*.whl

ENV FLASK_APP=sardadmin
COPY docker/entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

CMD python3 -m flask run
