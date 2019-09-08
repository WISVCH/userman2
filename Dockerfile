FROM node AS node

WORKDIR /src
COPY . .
RUN yarn install --flat

FROM python:3.6-stretch

# CH CA certificate for LDAP connections
RUN curl -so /usr/local/share/ca-certificates/wisvch.crt https://ch.tudelft.nl/certs/wisvch.crt && \
    chmod 644 /usr/local/share/ca-certificates/wisvch.crt && \
    update-ca-certificates

RUN mkdir -p /srv
WORKDIR /srv
COPY . /srv
COPY --from=node /src/userman2/static/lib /srv/userman2/static/lib

RUN export DEBIAN_FRONTEND="noninteractive" && \
    apt-get update && \
    apt-get install -y --no-install-recommends libldap2-dev libsasl2-dev && \
    pip install --no-cache-dir -r requirements.txt ddtrace gunicorn && \
    cp userman2/local.py.example userman2/local.py && \
    ./manage.py collectstatic --noinput && \
    apt-get purge -y libldap2-dev libsasl2-dev && \
    apt-get autoremove -y && \
    rm -rf userman2/local.py* /tmp/* /var/lib/apt/lists/* && \
    ln -s /config/local.py userman2/local.py

RUN groupadd -r userman2 --gid=999 && useradd --no-log-init -r -g userman2 --uid=999 userman2
USER 999

ENTRYPOINT ["/srv/docker-entrypoint.sh"]
CMD ["gunicorn"]
EXPOSE 8000

LABEL quay.expires-after=12w
