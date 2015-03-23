# Getting Started from scratch

The following process assumes that the devopment envirmonment alread has the following items installed:

    Python 2.7.x
    virtualenv & pip
    Git
    MySQL (recommended) or PostreSQL/PostGIS

# The Steps

## 0. Create Database

Use either MySQL (recommended) or PostreSQL/PostGIS and create a new database named `AIMS`

## 1. Create AIMS project directory

    mkdir ~/projects/
    mkdir ~/projects/aims


## 2. Create virtualenv and activate

    cd ~/projects/aims
    virtualenv env
    source env/bin/activate


## 3. Clone Catalpa's fork of OIPA

    git clone https://github.com/catalpainternational/OIPA
    git checkout v2


## 4. Intall OIPA requirements

    pip install -r OIPA/OIPA/requirements.txt


## 5. Install AIMS as an environment dependency with local source

    pip install -e git+https://github.com/catalpainternational/MohingaV1.git\#egg\=aims


## 6. Install AIMS requiments

    cd ~/projects/aims/env/src/aims
    pip install -r requirements.txt


## 7. Copy over settings and urls to OIPA instance

    cp deploy/urls.py.example ~/projects/aims/OIPA/OIPA/OIPA/urls.py
    cp deploy/settings.py.example ~/projects/aims/OIPA/OIPA/OIPA/settings.py
    cp deploy/local_settings.py.example ~/projects/aims/OIPA/OIPA/OIPA/local_settings.py


## 8. Configure Database settings

Use your favorite text editor to edit `DATABASE` in `local_settings.py`. 
Add your database settings and save.

    nano ~/projects/aims/OIPA/OIPA/OIPA/local_settings.py


## 9. Initialize the database

    cd ~/projects/aims/OIPA/OIPA
    python manage.py syncdb
    python manage.py loaddata ~/projects/aims/env/src/aims/fixtures/initial.json

## 10. Run server and Open up a browser and See if it worked!

    python manage.py runserver    
    open http://127.0.0.1:8000 -a safari

