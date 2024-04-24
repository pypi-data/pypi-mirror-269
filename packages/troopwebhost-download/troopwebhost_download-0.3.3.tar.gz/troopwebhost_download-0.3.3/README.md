# troopwebhost-downloader

Downloads the troopwebhost files needed to feed into flask-troop

Instructions:

copy .env.example to .env

change .env to be user-readable only (chmod go-r .env)

log in to troopwebhost and inspect the page, look at the cookies and find the value for the cookie stored with "application_ID"

edit .env to use your username and password and your application_ID for your troop

run export.py

resulting csv files will be in output/


command-line:


