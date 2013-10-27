cd /srv/www/userman
chown -R www-userman:www-userman *
chmod -R o-rX *; chmod o+rX static static/*
setfacl -m u:www-data:rX userman2