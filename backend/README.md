# Smart-Clinic

## Preparation

Install [Git](https://git-scm.com/downloads)

Install [python 3.8.6](https://www.python.org/downloads/release/python-386/) or higher. 
> Remember to check the box for editing PATH variable during python installation process.

Install [MariaDB](https://www.mariadbtutorial.com/getting-started/install-mariadb/)
> Make sure to remember password that you've set during installation process.

## Cloning repo

1. Open console and navigate to the directory you want to clone the repo.
2. Run this command  
`git clone https://gitlab.com/vista-med/backend.git`
3. Navigate to the created folder  
`cd smart_clinic/`
3. Run  
`git config user.name "USERNAME"`  
USERNAME - any username you want.
4. Run  
`git config user.email "USEREMAIL"`  
USEREMAIL - your email from gitlab.

## Set up
1. If not already, open up terminal and navigate to the project directory
2. Create virtual environment by running:
On macOS and Linux:  
`python3 -m venv venv`

    On Windows:  
`py -m venv venv`
3. Activate virtual environment

    On macOS and Linux:  
`source venv/bin/activate`

    On Windows:  
`. venv/Scripts/activate`
4. Install python dependencies  
`pip install -r requirements.txt`
5. Create [database](https://mariadb.com/kb/en/create-database/) for MariaDB  

    TODO detailed description

> Or try using GUI software like Navicat, DBeaver, etc. 
6. Inside project folder go to 'smart_clinic', there you should create new file named "local_settings.py" 
7. Copy code from "local_settings_example.py" to newly created file. There you might see an instructions on how to set up project on your local machine, follow them
8. Change database name and credentials to the ones you've created earlier.
9. Go back to the project folder  
`cd ../`
10. Run the following commands one by one  
`python manage.py collectstatic`  
`python manage.py migrate`  
`python manage.py createsuperuser`  
`python manage.py runserver`
11. In separate terminal you can run frontend server  
`npm start`
12. Now you can signin with the superuser you've created or sign up as a new user. 
