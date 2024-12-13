## PostgreSQL Setup Guide

This guide will help you setup PostgreSQL for your server.

1. Login as superuser in PostgreSQL.
2. Create a user in PostgreSQL with the following command.

    ```sql
    CREATE USER yojana_db_user WITH LOGIN PASSWORD 'Yoj@na@321';
    ```

3. Setup default encoding and locale for the user.

    ```sql
    ALTER ROLE yojana_db_user SET client_encoding TO 'utf8';
    ALTER ROLE yojana_db_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE yojana_db_user SET timezone TO 'UTC';
    ```

4. Create a database for the user and grant access to it.

    ```sql
    CREATE DATABASE yojana_db WITH OWNER yojana_db_user;
    GRANT ALL PRIVILEGES ON DATABASE yojana_db TO yojana_db_user;
    ```
