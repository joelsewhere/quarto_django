echo -e "\n\n\x1B[1;42mMaking Django Database Migrations\x1B[0m\n\n"
python django_site/manage.py makemigrations quarto
python django_site/manage.py migrate
python django_site/manage.py makemigrations
python djnago_site/manage.py migrate

SUPERUSER=false
case "$1" in
-s)
   SUPERUSER=true
   ;;
esac
if $SUPERUSER
then
    echo -e "\n\n\x1B[1;42mRunning Django createsuperuser Application\x1B[0m\n\n"
    python django_site/manage.py createsuperuser
fi
bash bin/run.sh


