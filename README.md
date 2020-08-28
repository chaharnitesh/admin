
Django wallet app


# Create a virtual environment
sudo apt install python3-venv
python3 -m venv <name>

# Activate venv 
source <name>/bin/activate


# Install necessary Python packages including Django
pip3 install -r requirements.txt

#Now, install postgreSQL and its required package
sudo apt-get install postgresql postgresql-contrib

#create a database user and database for our Django application
sudo su - postgres

#Now, you are logged in as postgres user. lets create database user and assign necessary privileges to it
createuser --interactive -P


#Give a appropraite name to database as well, as per your Django application
createdb --owner <databseuser> <databasename>

# perform all migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
python manage.py runserver
