California Civic Lab Disclosure Backend
==================================================

## Setup

1. Install python and pip
2. `sudo pip install virtualenv`
3. `virtualenv env`
4. `source env/bin/activate` (you will have to do this every time you want to
   start working)
5. `pip install -r requirements.txt`
6. install mysql

## Dependencies

If you've worked with Django and python before, these steps should be familiar to you.

### Virtualenv

You'll need python, pip, virtualenv.

#### Mac

Python 2.7.9 includes pip:

```
brew install python
pip install virtualenv
```




### MySQL

#### Install mysql

```
    Mac: brew install mysql
```

alternate method for mac with macports
```
sudo port install mysql56, mysql56-server
sudo port select mysql mysql56
sudo -u _mysql mysql_install_db 
sudo chown -R _mysql:_mysql /opt/local/var/db/mysql56/ 
sudo chown -R _mysql:_mysql /opt/local/var/run/mysql56/ 
sudo chown -R _mysql:_mysql /opt/local/var/log/mysql56/
sudo port load mysql56-server
ps -ax | grep mysql
# Should return filepath to mysql56
/opt/local/lib/mysql56/bin/mysqladmin -u root -p password 
# Leave the password blank
# Start the server
mysql -u root -p
# Exit the server
exit;

# This command will Stop the server
# sudo port unload mysql56-server
```
https://trac.macports.org/wiki/howto/MySQL

#### Download the mysqld package for python 
#### MySQL-python-1.2.5
https://pypi.python.org/pypi/MySQL-python/1.2.5
http://mysql-python.sourceforge.net/MySQLdb.html

```
pip install MySQL-python-1.2.5.zip
```

#### Prepare the database

```
mysql --user root
mysql> create database calaccess_raw;
mysql> \q
python disclosure-backend/manage.py migrate
```

#### if ^ returns an error, make sure that the data is sync'd properly
```
python disclosure-backend/manage.py syncdb
```


## Download the data

First, a basic data check to make sure things are working:

    $ python disclosure-backend/manage.py downloadcalaccessrawdata --use-test-data

### Zipcode/metro data

    $ python disclosure-backend/manage.py downloadzipcodedata

### Netfile

Netfile contains campaign finance data for a number of jurisdictions. Not all
jurisdictions will have data.

    $ python disclosure-backend/manage.py downloadnetfilerawdata

### Cal-Access

Cal-Access is the state data. It's ~750MB of data and takes about an hour to
trim, clean and process.

    $ python disclosure-backend/manage.py downloadcalaccessrawdata

## Deploying

```
ssh opencal.opendisclosure.io /usr/local/bin/deploy-backend
```
