# npmt-dev
Formal development of npmt-tool.


1. This is a django based project.
2. Uses PostgreSQL for database.
3. Uses leaflet for openstreet map rendering and handling.

This document may not be always updated. Ask the developers to update if something is missing.


Database setup:

To install postgres and db components (refer here):
> `sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib`

If server is not running, use this command:
> `sudo /etc/init.d/postgresql restart`

If that doesn't work, try purging and reinstalling:

`sudo apt-get remove --purge postgresql-9.5`


`sudo apt-get install postgresql`

Switch user to postgres

`sudo su - postgres`

`psql`

```
postgres=# create database npmtapp;
CREATE DATABASE
postgres=# create user npmtapp_user with password 'npmt@app';
CREATE ROLE
postgres=# ALTER ROLE npmtapp_user SET client_encoding TO 'utf8';
ALTER ROLE
postgres=# ALTER ROLE npmtapp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE
postgres=# ALTER ROLE npmtapp_user SET timezone TO 'UTC';
ALTER ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE npmtapp TO npmtapp_user;
GRANT
```
