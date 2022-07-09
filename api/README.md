# abc_school_api

REST API created with flask micro-framework for primary school taking student management system

## postgres

create owner : create user abc_admin with password 'abc_admin';
create database : create database abc_school_api_db owner abc_admin;

## migration

$ flask db init
$ flask db migrate -m "Initial migration."
$ flask db upgrade.
