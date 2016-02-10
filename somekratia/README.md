# somekratia
Design of WWW services


OS X ohjeet

- Lataa Postgress.app http://postgresapp.com
  - Kopioi Applications kansioon 
  - Aja ja avaa tietokannan konsoli (Klikkaa norsua yläpalkissa ja valitse 'Open psql'). Luo tietokanta ja käyttäjä:
    (Ohjeet osoitteesta http://www.cyberciti.biz/faq/howto-add-postgresql-user-account/)
    - \d template1
    - CREATE USER somekratia WITH PASSWORD extemporizers735!laboriously
    - CREATE DATABASE somekratia;
    - GRANT ALL PRIVILEGES ON DATABASE somekratia to somekratia;
    - \q
  
- Lataa Python 3.5 https://www.python.org/downloads/release/python-350/
- Lataa PyCharm Professional Edition https://www.jetbrains.com/pycharm/download/ (vaatii javan)
  - Pyydä opiskelijalisenssi osoitteesta https://www.jetbrains.com/student/
  
- Avaa PyCharm ja kloonaa projekti GitHubista
  - https://www.jetbrains.com/pycharm/help/cloning-a-repository-from-github.html

- PyCharm valikosta valitse Tools->Run manage.py task ja suorita seuraavat komennot 
  - makemigrations
  - migrate
  - createsuperuser (seuraa ohjeita)
  - runserver (serveri pyörii ja selaimella pitäisi päästä osoitteeseen http://localhost:8000/admin/)
  - kirjaudu hetki sitten luoduilla tunnuksilla
  
  
