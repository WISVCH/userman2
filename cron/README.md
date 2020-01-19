# Userman cron component

Setup:
```
# Debian Jessie, Stretch:
apt-get -y install python3-pip libldap2-dev libsasl2-dev
pip3 install python-ldap
# Debian Buster:
apt-get -y install python3-ldap

cd /usr/local
git clone git@github.com:WISVCH/userman2.git
cd userman2/cron
ln -s ../configs/config-<hostname>.py config.py
cat > /etc/cron.d/userman2 <<EOF
# Regelmatig het systeem accounts laten aanmaken / aanpassen / verwijderen
*/3 * * * *     root    flock -n /var/run/userman2 /usr/local/userman2/cron/checkldap.py
EOF
```