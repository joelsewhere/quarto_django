echo -e "\n\n\x1B[0m\x1B[1;42mRunning quarto render\x1B[0m\n\n"
quarto render
echo  -e "\n\n\x1B[1;42mLaunching Django Application\x1B[0m\n\n"
python django_site/manage.py runserver